#####################################
# write_links_cont_person

# Input: 	person_lookup.json
# 			pages_links_en.ttl

# Output:	filtered_links.txt

# Description:
# Build a list that contains all links between two persons (unlabled)
#####################################

import json
import sys

def write_links_cont_person():
	try:
		f_json = open('data_extracted/person_lookup.json','r',encoding="utf8")
	except IOError:
		print('Need to create person_lookup.json first. (Execute write_personlist_by_type.py)')

	person_lookup = json.load(f_json)
	f_json.close()

	f_in = open('data_raw/page_links_en.ttl','r', encoding="utf8")
	f_out = open('data_extracted/filtered_links.txt','w+', encoding="utf8")

	c=0
	next(f_in) #First Line is comment with date
	for line in f_in:
		splits=line.split()
		subject=splits[0]
		value=splits[2]
		if person_lookup.get(subject)==True and person_lookup.get(value)==True:
			f_out.write(subject[-1:1]+" "+value[-1:1]+"\n")


	f_in.close()
	f_out.close()

	print('DONE!')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	write_links_cont_person()