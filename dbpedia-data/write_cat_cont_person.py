#####################################
# write_cat_cont_person

# Input: 	person_lookup.json
# 			article_categories_en.ttl

# Output:	cat_assignment.json (dict that matches "DBpediaURL" -> [*categories*])
# 			filtered_category.txt (human readable, same content, for debug purposes)

# Description:
# Build a dictionary that contains all categories assigned to a person based on DBpedia's dataset
# Maps: "page of person" -> list of assigned categories

# @author: mreif
#####################################

import json
import sys

def write_cat_cont_person():
	try:
		f_json = open('data_extracted/person_lookup.json','r',encoding="utf8")
	except IOError:
		print('Need to create person_lookup.json first. (Execute write_personlist_by_type.py)')

	# Load person lookup created by write_personlist_by_type.py (Maps: *page of person* -> True, if it is a Person)
	person_lookup = json.load(f_json)
	print("Load complete: person_lookup.json")
	f_json.close()

	cat_assignment = dict()

	f_in = open('data_raw/article_categories_en.ttl','r', encoding="utf8")
	f_out = open('data_extracted/filtered_category.txt','w+', encoding="utf8")
	
	next(f_in) #First Line is comment with date
	for line in f_in:
		# Read all category assignments
		splits=line.split()
		person=splits[0]
		if person_lookup.get(person)==True:
			person=person[1:-1]
			cat=splits[2].split('Category:')[1][:-1].lower()
			# If it category belongs to a person page, add it to the list of categories
			if cat_assignment.get(person)==None:
				cat_assignment[person]=[cat]
			else:
				cat_assignment[person].append(cat)
			f_out.write(person + '\t' + cat + '\n')

	f_in.close()
	f_out.close()

	with open('data_extracted/cat_assignment.json','w+', encoding='utf8') as f_json:
		json.dump(cat_assignment, f_json, ensure_ascii=False)

	print('write_cat_cont_person - DONE')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	write_cat_cont_person()