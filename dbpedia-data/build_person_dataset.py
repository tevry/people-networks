#####################################
# build_person_dataset

# Input:	prop_selection.txt
#			gender_assignment.json
#			wikilinks_assignment.json

# Output:	person_data.tsv (combination of raw DBpedia values)

# Description:
# Build the actual dataset out of the unaltered DBpedia property values.
# Contains all persons. Result is rather incomplete and needs improvement.

# @author: mreif
#####################################

import json
import sys

def build_person_dataset():

	try:
		f_in = open('prop_selection.txt','r', encoding="utf8")
	except IOError:
		print('Please create prop_selection.txt')
	
	prop_categories=[]
	for line in f_in:
		prop_categories.append(line.strip())
	print("Load complete: prop_selection.txt")
	f_in.close()

	try:
		f_json = open('data_extracted/prop_assignment.json','r',encoding="utf8")
	except IOError:
		print('Need to create prop_assignment.json first. (Execute preselect_properties.py)')

	property_assignment = json.load(f_json)
	print("Load complete: property_assignment.json")
	f_json.close()

	try:
		f_json = open('data_extracted/gender_assignment.json','r',encoding="utf8")
	except IOError:
		print('Need to create gender_assignment.json first. (Execute write_gender_cont_person.py)')

	gender_assignment = json.load(f_json)
	f_json.close()
	print("Load complete: gender_assignment.json")

	try:
		f_json = open('data_extracted/wikilinks_assignment.json','r',encoding="utf8")
	except IOError:
		print('Need to create wikilinks_assignment.json first. (Execute write_wikilinks_cont_person.py)')

	wikilinks_assignment = json.load(f_json)
	f_json.close()
	print("Load complete: wikilinks_assignment.json")

	print("Start building")
	f_out = open('data_extracted/person-data.tsv','w+',encoding='utf-8')
	
	#Desired Formatting: dbpediaURL \t ID \t wikilink \t gender \t  *(properties + \t)* \n

	person_id_map=dict()

	#Print headline
	f_out.write("#DBpURL\tID\tWikiURL\tgender")
	for prop in prop_categories:
		f_out.write("\t"+prop)
	f_out.write("\n")

	ID=1
	for person, assigned_props in property_assignment.items():
		# Iteratve over all person urls and the assigned props and add an ID
		person_id_map[person]=ID
		f_out.write(person+'\t'+str(ID))

		wikilink_value=wikilinks_assignment.get(person)
		#Try to assign wiki URL to each dbpedia URL (should always be possible)
		if wikilink_value==None:
			f_out.write('\t' + 'NA')
		else:
			f_out.write('\t' + wikilink_value)

		gender_value=gender_assignment.get(person)
		#Try to assign gender to each dbpedia URL (rather incomplete data)
		if gender_value==None:
			f_out.write('\t' + 'NA')
		else:
			f_out.write('\t' + gender_value)

		# Assign all other props
		for prop in prop_categories:
			value = assigned_props.get(prop)
			if value==None:
				f_out.write('\t' + 'NA')
			else:
				f_out.write('\t' + str(value))

		f_out.write('\n')

		ID+=1

	f_out.close()
	print("build_person_dataset.py - DONE")


if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	build_person_dataset()