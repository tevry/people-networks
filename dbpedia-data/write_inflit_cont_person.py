#####################################
# write_inflit_cont_person

# Input: 	person_lookup.json
# 			mappingbased_literals_en.ttl

# Output:	filtered_inflit.txt (List of all (infobox) literales that are assigned to a person)

# Description:
# Build a list that contains the literal properties assigned to a person based on DBpedia's dataset
#####################################


import json
import sys

def write_inflit_cont_person():
	try:
		f_json = open('data_extracted/person_lookup.json','r',encoding="utf8")
	except IOError:
		print('Need to create person_lookup.json first. (Execute write_personlist_by_type.py)')

	person_lookup = json.load(f_json)
	f_json.close()

	f_in = open('data_raw/mappingbased_literals_en.ttl','r', encoding="utf8")
	f_out = open('data_extracted/filtered_inflit.txt','w+', encoding="utf8")
	
	next(f_in) #First Line is Comment with data (Remove if using multiple processes)
	for line in f_in:
		splits=line.split()
		subject=splits[0]
		if person_lookup.get(subject)==True:
			f_out.write(line)

	f_in.close()
	f_out.close()

	print('DONE!')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	write_inflit_cont_person()