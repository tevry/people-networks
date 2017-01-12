#####################################
# normalize_infobj_to_inflits

# Input:	person_lookup.json
#			infobj_to_lit_map.json
#			filtered_infobj.txt
#			

# Output:	infobj_transformed(inflit).txt (List of pure infobox literals)
#			infobj_transformed(links).txt (List of link labels between people)

# Description:
# Build a list of all infobox literals extracted from the infobox objects (including the resolution weird "__" links)
# Build a second list that describes the type of connection two people have
# Normalize the same formating for all literals

# @author: mreif
#####################################

import json
import sys

def normalize_infobj_to_inflits():
	try:
		f_json = open('data_extracted/person_lookup.json','r',encoding="utf8")
	except IOError:
		print('Need to create person_lookup.json first. (Execute write_personlist_by_type.py)')

	person_lookup = json.load(f_json)
	print("Load complete: person_lookup.json")
	f_json.close()

	try:
		f_json = open('data_extracted/infobj_to_lit_map.json','r',encoding="utf8")
	except IOError:
		print('Need to create infobj_to_lit_map.json first. (Execute write_inflit_cont_infobj.py)')

	infobj_to_lit = json.load(f_json)
	print("Load complete: infobj_to_lit_map.json")
	f_json.close()

	f_in = open('data_extracted/filtered_infobj.txt','r', encoding="utf8")
	f_out = open('data_extracted/infobj_transformed(inflit).txt','w+', encoding="utf8")
	f_out2 = open('data_extracted/infobj_transformed(links).txt','w+', encoding="utf8")
 
	for line in f_in:
		# Read all infobj relations that are on person pages
		splits=line.split()
		subject=splits[0]
		relation = splits[1]
		literal = splits[2]

		lookup_val=infobj_to_lit.get(literal)

		if lookup_val!=None:
			# If __ can be looked up, write the resolved value
			f_out.write(subject + " " + relation + " " + lookup_val +"\n")
		elif "__" in literal:
			# If __ still has not been resolved, continue
			continue
		elif person_lookup.get(literal)!=None:
			# If other assigned value is another person, write as links with values
			f_out2.write(line)
		else:
			# transform object into literal form and assign that
			lit_split = literal.split("/")
			f_out.write(subject + " " + relation + ' "' + lit_split[-1][:-1].replace('_',' ') + '"\n')
		
	f_in.close()
	f_out.close()
	f_out2.close()

	print('normalize_infobj_to_inflits - DONE')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	normalize_infobj_to_inflits()