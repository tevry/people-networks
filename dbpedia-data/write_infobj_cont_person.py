#####################################
# write_infobj_cont_person

# Input: 	person_lookup.json
# 			mappingbased_objects_en.ttl

# Output:	filtered_infobj.txt (List of all (infobox) links to other wikipedia pages)

# Description:
# Build a list that contains the infobox links to other wikipedia pages that are objects on their own.
# Filter only objects that contain at least one person based on DBpedia's dataset
# Note that DBpedia's dataset contains weird object links like "Johnny_Depp__1" that need to be resolved (write_infobj_needing_lookup.py)

# @author: mreif
#####################################

import json
import sys

def write_infobj_cont_person():
	try:
		f_json = open('data_extracted/person_lookup.json','r',encoding="utf8")
	except IOError:
		print('Need to create person_lookup.json first. (Execute write_personlist_by_type.py)')

	# Load person lookup created by write_personlist_by_type.py (Maps: *page of person* -> True, if it is a Person)
	person_lookup = json.load(f_json)
	print("Load complete: person_lookup.json")
	f_json.close()

	f_in = open('data_raw/mappingbased_objects_en.ttl','r', encoding="utf8")
	f_out = open('data_extracted/filtered_infobj.txt','w+', encoding="utf8")
	
	next(f_in) #First Line is comment with date
	for line in f_in:
		# Read mappingbased_objects (contains links to object pages, not literals) -> needs transformation or lookup
		splits=line.split()
		subject=splits[0]
		if person_lookup.get(subject)==True:
			# Only write objects if they belong to a page of a person
			f_out.write(line)

	f_in.close()
	f_out.close()

	print('write_infobj_cont_person - DONE')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	write_infobj_cont_person()