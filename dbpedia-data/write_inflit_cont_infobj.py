#####################################
# write_inflit_cont_infobj

# Input:	infobj_lookup.json

# Output:	infobj_to_lit_map.json (dict that matches "DBpediaURL containing __" -> "actual property value")
# 			filtered_inflit_infobj.txt (human readable, same content, for debug purposes)

# Description:
# Looks up the "__" objects, resolves all the actual infobox literals and stores it in a dict.
#
# e.g. "Johnny_Depp"'s occupation is linked to "Johnny_Depp__1"
# the actual literal property can be found in the "title" of that page and gets resolved

# @author: mreif
#####################################

import json
import sys

def write_inflit_cont_infobj():
	try:
		f_json = open('data_extracted/infobj_lookup.json','r',encoding="utf8")
	except IOError:
		print('Need to create infobj_lookup.json first. (Execute write_infobj_cont_needing_lookup.py)')

	infobj_lookup = json.load(f_json)
	print("Load complete: infobj_lookup.json")
	f_json.close()

	f_in = open('data_raw/mappingbased_literals_en.ttl','r', encoding="utf8")
	f_out = open('data_extracted/filtered_inflit_infobj.txt','w+', encoding="utf8")
	
	infobj_to_lit_map = dict()

	next(f_in) #First Line is Comment with data (Remove if using multiple processes)
	for line in f_in:
		# Read all literals
		splits=line.split()
		subject=splits[0]
		prop = splits[1]
		literal = splits[2:]
		if prop=='<http://dbpedia.org/ontology/title>' and infobj_lookup.get(subject)==True:
			# If it is the title of one of the '__' person properties determined in write_infobj_needing_lookup, add it to a lookup dict
			f_out.write(line)
			infobj_to_lit_map[subject]=' '.join(literal)

	f_in.close()
	f_out.close()

	with open('data_extracted/infobj_to_lit_map.json','w+', encoding='utf8') as f_json:
		json.dump(infobj_to_lit_map, f_json, ensure_ascii=False)

	print('write_inflit_cont_infobj - DONE')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	write_inflit_cont_infobj()