#####################################
# write_wikilinks_cont_person

# Input: 	person_lookup.json
# 			wikipedia_links_en.ttl (maps dbpedia URL to wikipedia URL)

# Output:	wikilinks_assignment.json (dict that matches "DBpediaURL" -> "wikiURL")
# 			filtered_wikilinks.txt (human readable, same content, for debug purposes)

# Description:
# Build a list that matches DBpedia URL to wikpedia URL for every person

# @author: mreif
#####################################

import json
import sys

def write_wikilinks_cont_person():
	try:
		f_json = open('data_extracted/person_lookup.json','r',encoding="utf8")
	except IOError:
		print('Need to create person_lookup.json first. (Execute write_personlist_by_type.py)')

	# Load person lookup created by write_personlist_by_type.py (Maps: *page of person* -> True, if it is a Person)
	person_lookup = json.load(f_json)
	print("Load complete: person_lookup.json")
	f_json.close()

	f_in = open('data_raw/wikipedia_links_en.ttl','r', encoding="utf8")
	f_out = open('data_extracted/filtered_wikilinks.txt','w+', encoding="utf8")
	
	wikilinks_assignment=dict()

	next(f_in) #First Line is comment with date
	for line in f_in:
		# Read wikilinks
		splits=line.split()
		subject=splits[0]
		value=splits[2]
		if person_lookup.get(subject)==True:
			#If it belongs to a person entitly keep it
			f_out.write(line)
			wikilinks_assignment[subject[1:-1]]=value[1:-1]

	f_in.close()
	f_out.close()

	with open('data_extracted/wikilinks_assignment.json','w+', encoding='utf8') as f_json:
		json.dump(wikilinks_assignment, f_json, ensure_ascii=False)

	print('write_wikilinks_cont_person - DONE')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	write_wikilinks_cont_person()