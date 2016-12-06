#####################################
# preselect_properties

# Input:	literals_final.txt
#			prop_selection.txt (handmade)

# Output:	property_assignment.json (2 nested dicts, that match like "DBpediaURL" -> "Property Name" -> [*"Property Value"*])
# 			properties_final.txt (human readable, same content, for debug purposes)

# Description:
# Take all wanted properties defined in prop_selection and filter the literals. Add multiple values of a property to a list.
# Store the the list by property name per person.
#####################################

import json
import sys

def clean_value(value):
	value=value.replace('"',' ') #Remove Quotes
	value=value.split('@en')[0] # Remove "@en"
	value=value.replace('"',' ') #Remove leading / tailing whitespace
	return value

def preselect_properties():

	f_in = open('prop_selection.txt','r', encoding="utf8")
	prop_filter=set()
	for line in f_in:
		prop_filter.add(line.strip())
	f_in.close()

	f_in = open('data_extracted/literals_final.txt','r', encoding="utf8")
	f_out = open('data_extracted/properties_final.txt','w+', encoding="utf8")
	
	prop_assignment=dict()

	for line in f_in:
		splits=line.split()
		subject=splits[0]
		prop=splits[1]
		value=" ".join(splits[2:])

		if prop in prop_filter:
			f_out.write(line)
			if prop_assignment.get(subject)==None:
				prop_assignment[subject]=dict()
				prop_assignment[subject][prop]=[clean_value(value)]
			else:
				if prop_assignment.get(subject).get(prop)==None:
					prop_assignment[subject][prop]=[clean_value(value)]
				else:
					prop_assignment[subject][prop].append(clean_value(value))

	f_in.close()
	f_out.close()

	with open('data_extracted/prop_assignment.json','w+', encoding='utf8') as f_json:
		json.dump(prop_assignment, f_json, ensure_ascii=False)

	print('DONE!')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	preselect_properties()