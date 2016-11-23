#####################################
# improve_person_dataset_cat

# Input:	prop_selection.txt
#			person_data.tsv
#			cat_assignment.json

# Output:	cat-improved-person_data.tsv

# Description:
# Extend the property assignment of DBpedia with values extracted from the categories
# Currently Improving: Gender, Occupations, Nationality
#####################################

import json
import sys
import ast

def improve_person_dataset_cat():
	try:
		f_json = open('data_extracted/cat_assignment.json','r',encoding="utf8")
	except IOError:
		print('Need to create cat_assignment.json first. (Execute write_cat_cont_person.py)')
	cat_assignment = json.load(f_json)
	f_json.close()
	print("Load complete: cat_assignment.json")

	#Get indeces of used props
	try:
		f_in = open('prop_selection.txt','r', encoding="utf8")
	except IOError:
		print('Please create prop_selection.txt')

	prop_to_index=dict()
	index_to_prop=dict()
	# 0 is page name, 1 is ID, 2 is wikilink, 3 is gender, 4ff are props
	c=3
	prop_to_index['gender']=c
	index_to_prop[c]='gender'
	c=4
	for line in f_in:
		prop_to_index[line.strip()]=c
		index_to_prop[c]=line.strip()
		c+=1
	f_in.close()

	#Get List of scientist occupations
	try:
		f_in = open('data_raw/scientist-professions.txt','r', encoding="utf8")
	except IOError:
		print('Please create data_raw/scientist-professions.txt')
	sc_occupation_list=[]
	for line in f_in:
		sc_occupation_list.append(line.strip().lower())
	f_in.close()
	print('Load complete: scientist-professions.txt')

	#Get List of sport occupations
	try:
		f_in = open('data_raw/sport-professions.txt','r', encoding="utf8")
	except IOError:
		print('Please create data_raw/sport-professions.txt')
	sport_occupation_list=[]
	for line in f_in:
		sport_occupation_list.append(line.strip().lower())
	f_in.close()
	print('Load complete: sport-professions.txt')

	#Get List of all occupations
	try:
		f_in = open('data_raw/occupations.csv','r', encoding="utf8")
	except IOError:
		print('Please create data_raw/occupations.csv')
	occupation_list=[]
	for line in f_in:
		occupation_list.append(line.strip().lower())
	f_in.close()
	print('Load complete: occupations.csv')

	#Get List of all nationalities
	try:
		f_in = open('data_raw/countries.csv','r', encoding="utf8")
	except IOError:
		print('Please create data_raw/countries.csv')
	nation_lookup=dict()
	f_in.readline()
	for line in f_in:
		splits=line.split(',')
		nation=splits[3].strip().lower()
		nation_terms=[term.lower().strip() for term in splits[4:]]
		#print(nation + '->' +str(nation_term))
		for term in nation_terms:
			nation_lookup[term]=nation
	f_in.close()
	print('Load complete: countries.csv')

	test_flag=False #PLS REMOVE LATER

	f_in= open('data_extracted/person-data.tsv','r',encoding="utf8")
	f_out= open('data_extracted/cat-improved-person-data.tsv','w+',encoding="utf8")

	#Copy Column Header
	f_out.write(f_in.readline())

	# This should probably be computed in parallel
	c=0
	for line in f_in:
		if (c%1000==0): 
			print(c,end="\r")
		splits=line.strip().split('\t')
		person=splits[0]
		
		if person=='http://dbpedia.org/resource/Johnny_Depp':
			test_flag=True

		categories=cat_assignment.get(person)
		if categories!=None:

			if test_flag==True:
				print(categories)

			# Gender Improvement - Preperation
			gender=splits[prop_to_index.get('gender')]
			if (splits[prop_to_index.get('gender')]=='NA'):
				w=0
				m=0

			# Occupation Improvement - Preperation
			assigned_occupation=splits[prop_to_index.get('occupation')]
			if assigned_occupation=='NA':
				assigned_occupation=[]
			else:
				assigned_occupation=ast.literal_eval(assigned_occupation)

			# Nationality Improvement - Preperation
			assigned_nationality=splits[prop_to_index.get('nationality')]
			if assigned_nationality=='NA':
				assigned_nationality=[]
			else:
				assigned_nationality=ast.literal_eval(assigned_nationality)


			for cat in categories:
				# Gender Improvement - Computation
				if (splits[prop_to_index.get('gender')]=='NA'):
					if ('female' in cat) or ('_woman_' in cat) or ('_women_' in cat) or (cat.startswith('woman_')) or (cat.startswith('women_')):
						w+=1
					elif ('male' in cat) or ('_man_' in cat) or ('_men_' in cat) or (cat.startswith('man_')) or (cat.startswith('men_')):
						m+=1

				#Occupation Improvement - Computation
				for occupation in sc_occupation_list:
					if not (occupation in assigned_occupation) and (occupation in cat.lower()):
						if test_flag==True:
							print(occupation + ' found in '+ cat)
						assigned_occupation.append(occupation)
						if not('scientist' in assigned_occupation):
							assigned_occupation.append('scientist')

				for occupation in sport_occupation_list:
					if not (occupation in assigned_occupation) and (occupation in cat.lower()):
						if test_flag==True:
							print(occupation + ' found in '+ cat)
						assigned_occupation.append(occupation)
						if not('sportsperson' in assigned_occupation):
							assigned_occupation.append('sportsperson')
			
				for occupation in occupation_list:
					if not (occupation in assigned_occupation) and (occupation in cat.lower()):
						if test_flag==True:
							print(occupation + ' found in '+ cat)
						assigned_occupation.append(occupation)

				#Nationality Improvement - Computation
				cat_splits=cat.split('_')

				term=cat_splits[0] #Only Check something like 'American_actor_in_the_1900'
				if nation_lookup.get(term)!=None and not(term in assigned_nationality):
						assigned_nationality.append(term)

				#for term in cat_splits:
				#	if nation_lookup.get(term)!=None and not(term in assigned_nationality):
				#		assigned_nationality.append(term)

			# Gender Improvement - toString
			if (w==0 and m==0) or m==w:
				gender='NA'
			elif w>m:
				gender='"female"@en'
			else:
				gender='"male"@en'

			# Occupation Improvement - toString
			if assigned_occupation==[]:
				assigned_occupation='NA'
			else:
				assigned_occupation=str(assigned_occupation)
				if test_flag==True:
					print(assigned_occupation)

			# Nationality Improvement - toString
			if assigned_nationality==[]:
				assigned_nationality='NA'
			else:
				assigned_nationality=str(assigned_nationality)
				if test_flag==True:
					print(assigned_nationality)

		# Rewrite line
		f_out.write(splits[0]+'\t'+splits[1]+'\t'+splits[2])
		for i in range(3,len(splits)):
			if index_to_prop.get(i)=='gender':
				f_out.write('\t'+gender)
				if test_flag==True:
					print(gender)
			elif index_to_prop.get(i)=='occupation':
				f_out.write('\t'+assigned_occupation)
				if test_flag==True:
					print(assigned_occupation)
			elif index_to_prop.get(i)=='nationality':
				f_out.write('\t'+assigned_nationality)
				if test_flag==True:
					print(assigned_nationality)
			else:
				f_out.write('\t'+splits[i])
		f_out.write('\n')

		test_flag=False
		c+=1

	f_in.close()
	f_out.close()



if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	improve_person_dataset_cat()
