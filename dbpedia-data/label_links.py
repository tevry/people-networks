#####################################
# label_links

# Input:	linkprop_assignment.json
#			filtered_links.txt

# Output:	link-data.tsv

# Description:
# Joins all the the labeled links with the complete set of links between people
# -> Labels the links if possible

# @author: mreif
#####################################

import json
import sys

def label_links():

	try:
		f_json = open('data_extracted/linkprop_assignment.json','r',encoding="utf8")
	except IOError:
		print('Need to create linkprop_assignment.json first. (Execute preselect_properties.py)')
	linkproperty_assignment = json.load(f_json)
	f_json.close()
	print("Load complete: linkproperty_assignment.json")
	
	f_in = open('data_extracted/filtered_links.txt','r',encoding='utf-8')
	f_out = open('data_extracted/link-data.tsv','w+',encoding='utf-8')
	#Desired Formatting: Startperson \t Endperson \t Label \n

	for line in f_in:
		# Read all the links between people
		splits=line.split()
		start = splits[0][1:-1]
		end = splits[1][1:-1]
		
		# If this relation has a value assigned through a infobj, it gets a labeled relation, else it is unknown
		if  linkproperty_assignment.get(start)==None or linkproperty_assignment.get(start).get(end)==None:
			f_out.write(start + '\t' + end + '\tunknown\n')
		else:
			f_out.write(start + '\t' + end + '\t'+ str(linkproperty_assignment[start][end]) +'\n')

	f_out.close()
	f_in.close()
	print("label_links - DONE")

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	label_links()