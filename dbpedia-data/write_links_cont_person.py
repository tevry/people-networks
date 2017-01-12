#####################################
# write_links_cont_person

# Input: 	person_lookup.json
# 			pages_links_en.ttl

# Output:	filtered_links.txt

# Description:
# Build a list that contains all links between two persons (unlabled)

# @author: mreif
#####################################

import json
import sys

def write_links_cont_person():
	try:
		f_json = open('data_extracted/person_lookup.json','r',encoding="utf8")
	except IOError:
		print('Need to create person_lookup.json first. (Execute write_personlist_by_type.py)')

	# Load person lookup created by write_personlist_by_type.py (Maps: *page of person* -> True, if it is a Person)
	person_lookup = json.load(f_json)
	print("Load complete: person_lookup.json")
	f_json.close()

	f_in = open('data_raw/page_links_en.ttl','r', encoding="utf8")
	f_out = open('data_extracted/filtered_links.txt','w+', encoding="utf8")

	c=0
	next(f_in) #First Line is comment with date
	for line in f_in:
		# Read links (does not give a meaning to a link)
		splits=line.split()
		subject=splits[0]
		value=splits[2]
		if person_lookup.get(subject)==True and person_lookup.get(value)==True:
			# Only write the link if it is between 2 people
			f_out.write(subject[1:-1]+"\t"+value[1:-1]+"\n")


	f_in.close()
	f_out.close()

	print('write_links_cont_person - DONE')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	write_links_cont_person()