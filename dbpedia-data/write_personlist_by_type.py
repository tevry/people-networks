#####################################
# write_personlist_by_type

# Input:	instance_types_transitive_en.ttl

# Output:	person_lookup.json (dict that matches "DBpediaURL" -> True for easy lookup)
# 			personlist_manual.txt (human readable, same content, for debug purposes)

# Description:
# Build a lookup for each instance that is known as a "Person" in one of DBpedia's type systems
# Maps: *page of person* -> True, if it is a Person

# @author: mreif
#####################################

import json
import sys

def write_personlist_by_type():

	f_in = open('data_raw/instance_types_transitive_en.ttl','r', encoding="utf8")
	f_out = open('data_extracted/personlist_manual.txt','w+', encoding="utf8")

	unwanted=dict() # Filter dict
	# Filter:	- fictional characters (note: some are still in: Something like Miss Marple isnt tagged accordingly)
	# 			- the awkward entires ending "__1" (often duplicates of football players, famous people)
	#				-> the ones that are necessary will be looked up later

	person=dict() # Store all persons (unfiltered)

	final_dict=dict() # Dict for all persons that pass the filter (matches content of f_out)
	previous_subject=None # Dont add the same page multiple times

	# Read instance types
	for line in f_in:
		splits=line.split()
		subject=splits[0] # Read pagename
		value=splits[2] # Read type of that is assigned to that page

		if previous_subject==None:
			previous_subject=subject

		if value == '<http://dbpedia.org/ontology/FictionalCharacter>' or subject[-4:-2]=='__' or subject[-5:-3]=='__' or subject[-6:-4]=='__':
			# Filter fictional characters and '__' instances ( -> will be assigned later)
			unwanted[subject]=True

		if (value == '<http://dbpedia.org/ontology/Person>' or value == '<http://schema.org/Person>' or value == '<http://xmlns.com/foaf/0.1/Person>'):
			# Pages that are persons in one of the type systems
			person[subject]=True

		if previous_subject!=subject and unwanted.get(previous_subject)==None and person.get(previous_subject)==True :
			# If you switch to the next page object and it fits the criteria, write it
			f_out.write(previous_subject+"\n")
			final_dict[previous_subject]=True
			previous_subject=subject
		else:
			#Else skip it
			previous_subject=subject

	f_in.close()
	f_out.close()

	with open('data_extracted/person_lookup.json','w+', encoding='utf8') as f_json:
		json.dump(final_dict, f_json, ensure_ascii=False)

	print('write_personlist_by_type.py - DONE')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	write_personlist_by_type()