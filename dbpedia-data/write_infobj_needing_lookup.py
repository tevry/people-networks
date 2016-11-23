#####################################
# write_infobj_needing_lookup

# Input:	filtered_infobj.txt

# Output:	infobj_lookup.json (dict that matches "DBpediaURL" -> True for easy lookup)
# 			filtered_infobj_needing_lookup.txt (human readable, same content, for debug purposes)

# Description:
# Build a dict that enable lookup of infobox objects that contain "__"
#
# e.g. "Johnny_Depp"'s occupation is linked to "Johnny_Depp__1"
# the actual literal property can be found in the "title" of that page and needs to be resolved
#####################################

import json
import sys

def write_infobj_needing_lookup():

	f_in = open('data_extracted/filtered_infobj.txt','r', encoding="utf8")
	f_out = open('data_extracted/filtered_infobj_needing_lookup.txt','w+', encoding="utf8")
	
	infobj_lookup = dict()

	next(f_in) #First Line is comment with date
	for line in f_in:
		splits=line.split()
		subject=splits[0]
		ref=splits[2]
		if '__' in ref:
			infobj_lookup[ref]=True
			f_out.write(ref+'\n')

	f_in.close()
	f_out.close()

	with open('data_extracted/infobj_lookup.json','w+', encoding='utf8') as f_json:
		json.dump(infobj_lookup, f_json, ensure_ascii=False)

	print('DONE!')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	write_infobj_needing_lookup()