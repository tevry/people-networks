#####################################
# build_profession_datasets

# Input:	final-person-data.tsv

# Output:	actor-data.tsv	
# 			author-data.tsv	
# 			politician-data.tsv	
# 			sportsmen-data.tsv	
# 			scientist-data.tsv	

# Description:
# Split the data of all persons into the actual profession data sets that we are going to use.
#####################################

import json
import sys
import ast

def build_profession_datasets():

	f_in = open('final_datasets/final-person-data.tsv','r',encoding='utf-8')

	print("Start building")
	f_out_actor = open('final_datasets/actor-data.tsv','w+',encoding='utf-8')
	f_out_author = open('final_datasets/author-data.tsv','w+',encoding='utf-8')
	f_out_politician = open('final_datasets/politician-data.tsv','w+',encoding='utf-8')
	f_out_sportsmen = open('final_datasets/sportsmen-data.tsv','w+',encoding='utf-8')
	f_out_scientist = open('final_datasets/scientist-data.tsv','w+',encoding='utf-8')
	
	first_line=f_in.readline()
	f_out_actor.write(first_line)
	f_out_author.write(first_line)
	f_out_politician.write(first_line)
	f_out_sportsmen.write(first_line)
	f_out_scientist.write(first_line)

	# Read out the comment line 
	idToTag=dict()
	tagToInd=dict()
	ind = 0
	for tag in first_line[1:].strip().split("\t"):
		idToTag[ind]=tag
		tagToInd[tag]=ind
		ind+=1

	for line in f_in:
		splits = line.strip().split("\t")
		ind = tagToInd.get("occupation")
		
		if splits[ind]=="NA":
			continue
		occupations = ast.literal_eval(splits[ind])

		if ("actor" in occupations) or ("actress" in occupations):
			f_out_actor.write(line)
		if ("author" in occupations) or ("writer" in occupations):
			f_out_author.write(line)
		if "politician" in occupations:
			f_out_politician.write(line)
		if ("sportsperson" in occupations):
			f_out_sportsmen.write(line)
		if "scientist" in occupations:
			f_out_scientist.write(line)

	f_in.close()
	f_out_actor.close()
	f_out_author.close()
	f_out_politician.close()
	f_out_sportsmen.close()
	f_out_scientist.close()



if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	build_profession_datasets()