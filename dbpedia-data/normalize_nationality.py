#####################################
# normalize_nationality

# Input:	improved-person-data-v2.tsv

# Output:	final-person_data.tsv

# Description:
# Merges certain nationalities to have an easier selection later

# @author: mreif
#####################################

import json
import sys
import ast

def normalize_nationality():

	# Load countries and nationality clause that should be matched
	try:
		f_in = open('data_raw/countries.csv','r', encoding="utf8")
	except IOError:
		print('Please create data_raw/countries.csv')

	nationality_lookup=dict()
	nation_to_nationality=dict()

	f_in.readline()
	for line in f_in:
		splits=line.strip().split(',')
		nation=splits[3].split('(')[0].strip().lower()
		nationality=splits[4].replace('"',"").strip().lower()
		nationality_lookup[nationality]=True
		#If more than one nationality clause, match everything to the first one
		if len(splits)>5:
			for i in range(5,len(splits)):
				nationality_alt = splits[i].replace('"',"").strip().lower()
				nation_to_nationality[nationality_alt]=nationality
		nation_to_nationality[nation]=nationality
	f_in.close()
	print('Load complete: countries.csv')

	try:
		f_in = open('final_datasets/improved-person-data-v2.tsv','r', encoding="utf8")
	except IOError:
		print('Please create final_datasets/improved-person-data-v2.tsv (run improve_person_dataset_claudia)')
		return

	f_out= open('final_datasets/improved-person-data-v3.tsv','w+',encoding="utf8")

	#Copy Column Header
	firstLine = f_in.readline()
	f_out.write(firstLine)
	fl_splits = firstLine.split('\t') 

	# Find nationality column
	col=-1
	for i in range(0,len(fl_splits)):
		if fl_splits[i] == 'nationality':
			col=i
	if col==-1:
		print('Nationality property not found in the dataset')
		return
	
	for line in f_in:
		# Read all lines and get nationality tag
		splits=line.strip().split('\t')
		nationality_content=splits[col]
		if (nationality_content=='NA'):
			# if the nationality tag is "NA" just write the line and continue
			f_out.write(line)
			continue
		
		nationalities=ast.literal_eval(nationality_content) # Load nationaliy list
		for i in range(0,len(nationalities)):
			#Iterate over all assigned nationalites
			nationality=nationalities[i].strip().lower()
			if nation_to_nationality.get(nationality)!=None:
				# If a nationality fits, assign it
				nationalities[i]=nation_to_nationality.get(nationality)
				continue

			
			for word in nationality.split(' '):
				# Handle multi-word nationality tags
				if nationality_lookup.get(word[:-1])!=None:
					# Cases like "americans"
					nationalities[i]=word[:-1]
					continue
				if nationality_lookup.get(word)!=None:
					# Cases like "american citizen" -> american gets matched
					nationalities[i]=word
					continue
				if nation_to_nationality.get(word)!= None:
					# Cases like "citizen of germany"
					nationalities[i]=nation_to_nationality.get(word)
					continue

			#Hardcoded matches
			if nationality=="united kingdom" or nationality=="english people" or nationality=="uk":
				nationalities[i]='british'

			if nationality=="us citizen" or nationality=="united states" or nationality=="us" or ("united states" in nationality):
				nationalities[i]='american'

		#Remove Duplicates
		nationalities = list(set(nationalities))

		#Write Output
		f_out.write(splits[0])
		for ind in range(1,len(splits)):
			if ind == col:
				f_out.write("\t"+str(nationalities))
			else:
				f_out.write("\t"+str(splits[ind]))
		f_out.write("\n")


	f_in.close()
	f_out.close()

	print("normalize_nationality - DONE")



if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	normalize_nationality()
