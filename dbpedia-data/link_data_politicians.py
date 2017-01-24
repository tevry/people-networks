#####################################
# link_data_politicians

# Input:	filtered_links.tsv
#			politician-data.tsv

# Output:	link-data-politicians.tsv

# Description:
# Filters all links between politicians in the latest dataset

# @author: mreif
#####################################

import csv
import sys
import json

def link_data_politicians():

	# Load Scientist data
	scientist_lookup = dict()
	with open("final_datasets/politician-data.tsv", 'r', encoding="utf-8") as f_in:
		reader = csv.reader(f_in, delimiter='\t')
		firstLine = next(reader)
		for line in reader:
			dbpediaURL = line[0]
			wikiURL = line[2]
			scientist_lookup[dbpediaURL]=wikiURL

	f_in = open('data_extracted/filtered_links.txt','r', encoding="utf8")
	f_out = open('final_datasets/politician-link-data.tsv','w+', encoding="utf8")

	reader = csv.reader(f_in, delimiter='\t')
	c=0
	for line in reader:
		print("Reading: "+str(c), end = "\r")
		c+=1
		start_node=line[0]
		end_node=line[1]
		if scientist_lookup.get(start_node)!=None and scientist_lookup.get(end_node)!=None:
			# Only write the link if it is between 2 scientists
			f_out.write(scientist_lookup.get(start_node)+"\t"+scientist_lookup.get(end_node)+"\n")

	f_in.close()
	f_out.close()

	print('link_data_politicians - DONE')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	link_data_politicians()
