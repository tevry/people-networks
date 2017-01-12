#####################################
# improve_person_dataset_cat

# Input:	prop_selection.txt
#			person_data.tsv
#			cat_assignment.json
#			actor-professions.txt
#			politician-professions.txt
#			scientist-professions.txt
#			sport-professions.txt
#			writer-professions.txt
#			category_blacklist.txt
#			countries.csv

# Output:	cat-improved-person_data.tsv

# Description:
# Extend the property assignment of DBpedia with values extracted from the categories
# Currently Improving: Gender, Occupations, Nationality

# @author: mreif
#####################################

import json
import sys
import ast
import os

def load_occupations(path):
	try:
		f_in = open(path,'r', encoding="utf8")
	except IOError:
		print('Please create '+path)
	occupation_list=[]
	for line in f_in:
		occupation_list.append(line.strip().lower())
	f_in.close()
	print('Load complete: '+path)
	return occupation_list

def check_and_add_tag(cat, occupation_list, assigned_occupation, tag):
	for occupation in occupation_list:
		if not (occupation in assigned_occupation) and (occupation in cat.lower()):
			assigned_occupation.append(occupation)
			if not(tag in assigned_occupation):
				assigned_occupation.append(tag)
	return

def improve_person_dataset_cat(debug=False):
	try:
		f_json = open('data_extracted/cat_assignment.json','r',encoding="utf8")
	except IOError:
		print('Need to create cat_assignment.json first. (Execute write_cat_cont_person.py)')
	cat_assignment = json.load(f_json)
	f_json.close()
	print("Load complete: cat_assignment.json")

	try:
		f_in = open('prop_selection.txt','r', encoding="utf8")
	except IOError:
		print('Please create prop_selection.txt')

	#Get indeces of used props
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

	#Get List of occupations
	actor_occupation_list=load_occupations('data_raw/actor-professions.txt')
	politician_occupation_list=load_occupations('data_raw/politician-professions.txt')
	sc_occupation_list=load_occupations('data_raw/scientist-professions.txt')
	sport_occupation_list=load_occupations('data_raw/sport-professions.txt')
	writer_occupation_list=load_occupations('data_raw/writer-professions.txt')
	

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

	#Get List of blacklisted categories
	try:
		f_in = open('category_blacklist.txt','r', encoding="utf8")
	except IOError:
		print('Please create category_blacklist.txt')
	blacklist=dict()
	f_in.readline()
	for line in f_in:
		if line.startswith('\n') or line.startswith('#'):
			continue
		line=line.strip()
		blacklist[line]=True
	f_in.close()
	print('Load complete: category_blacklist.txt')

	if debug==True:
		print('Writing debug output enabled')
		os.makedirs(os.path.dirname('data_extracted/debug_occupation-matches.tsv'), exist_ok=True)
		deb_out = open('data_extracted/debug_occupation-matches.tsv','w+',encoding="utf8")
		deb_out_sc = open('data_extracted/debug_scientist-matches.tsv','w+',encoding="utf8")
		deb_out_sp = open('data_extracted/debug_sportsperson-matches.tsv','w+',encoding="utf8")

	f_in= open('data_extracted/person-data.tsv','r',encoding="utf8")
	f_out= open('data_extracted/improved-person-data-v1.tsv','w+',encoding="utf8")

	#Copy Column Header
	f_out.write(f_in.readline())

	#Remark: This should probably be computed in parallel
	c=0
	for line in f_in:
		if (c%1000==0): 
			print(c,end="\r")

		#Make sure that import is clean
		splits=line.strip().split('\t')
		splits = list( x.strip() for x in splits)

		person=splits[0]
		isFictional=False

		categories=cat_assignment.get(person)
		if categories!=None:

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
				assigned_occupation = list( x.strip() for x in assigned_occupation)
				if "*" in assigned_occupation:
					assigned_occupation.remove("*")

			# Nationality Improvement - Preperation
			assigned_nationality=splits[prop_to_index.get('nationality')]
			if assigned_nationality=='NA':
				assigned_nationality=[]
			else:
				assigned_nationality=ast.literal_eval(assigned_nationality)
				assigned_nationality = list( x.strip() for x in assigned_nationality)

			for cat in categories:
				if blacklist.get(cat.strip()):
					continue
				# If you a biography got a category starting with with "fictional_" 
				# assume it is a fictional character and don't write it
				if cat.startswith('fictional_'):
					isFictional=True
					break

				# Gender Improvement - Computation
				if (splits[prop_to_index.get('gender')]=='NA'):
					if ('female' in cat) or ('_woman_' in cat) or ('_women_' in cat) or (cat.startswith('woman_')) or (cat.startswith('women_')):
						w+=1
					elif ('male' in cat) or ('_man_' in cat) or ('_men_' in cat) or (cat.startswith('man_')) or (cat.startswith('men_')):
						m+=1

				#Occupation Improvement - Computation
				check_and_add_tag(cat, actor_occupation_list, assigned_occupation, 'actor')
				check_and_add_tag(cat, politician_occupation_list, assigned_occupation, 'politician')
				check_and_add_tag(cat, sc_occupation_list, assigned_occupation, 'scientist')
				check_and_add_tag(cat, sport_occupation_list, assigned_occupation, 'sportsperson')
				if debug==True and "player" in cat.lower():
					deb_out.write(cat+'\n')

				#Hardcoded "writer"-matching
				if not('writer' in assigned_occupation) and (('_writers' in cat.lower()) or ('writers_' in cat.lower())):
					assigned_occupation.append('writer')
				elif not ('songwriter' in cat.lower() or 'song_writer' in cat.lower()):
					check_and_add_tag(cat, writer_occupation_list, assigned_occupation, 'writer')

				#Nationality Improvement - Computation
				cat_splits=cat.split('_')
				term=cat_splits[0] #Only Check something like 'American_actor_in_the_1900'
				if nation_lookup.get(term)!=None and not(term in assigned_nationality):
						assigned_nationality.append(term)

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

			# Nationality Improvement - toString
			if assigned_nationality==[]:
				assigned_nationality='NA'
			else:
				assigned_nationality=str(assigned_nationality)

		if isFictional:
			continue

		# Rewrite line
		f_out.write(splits[0]+'\t'+splits[1]+'\t'+splits[2])
		for i in range(3,len(splits)):
			if index_to_prop.get(i)=='gender':
				f_out.write('\t'+gender)
			elif index_to_prop.get(i)=='occupation':
				f_out.write('\t'+assigned_occupation)
			elif index_to_prop.get(i)=='nationality':
				f_out.write('\t'+assigned_nationality)
			else:
				f_out.write('\t'+splits[i])
		f_out.write('\n')
		c+=1

	f_in.close()
	f_out.close()

	if debug==True:
		deb_out.close()
		deb_out_sc.close()
		deb_out_sp.close()

	print('improve_person_dataset_cat - DONE')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	improve_person_dataset_cat()
