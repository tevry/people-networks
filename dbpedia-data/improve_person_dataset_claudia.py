#####################################
# improve_person_dataset_claudia

# Input:	person_data_claudia.txt
#			cat-improved-person_data.tsv

# Output:	final-person_data.tsv

# Description:
# Improves the gender attribute and normalizes it.
# The additional data was provided by JProf. Dr. Claudia Wagner.

# @author: mreif
#####################################

import json
import sys

def improve_person_dataset_claudia():

	#Open dataset used for improvement
	try:
		f_in = open('data_raw/person_data_claudia.csv','r', encoding="utf8")
	except IOError:
		print('Please create data_raw/person_data_claudia.csv')

	dataset_lookup=dict()

	for line in f_in:
		# Read dataset and build gender lookup
		splits=line.strip().split(',')
		uri=splits[0]
		gender=splits[3]
		dataset_lookup[uri]=gender

	f_in.close()
	print('Load complete: person_data_claudia.csv')

	f_in= open('data_extracted/improved-person-data-v1.tsv','r',encoding="utf8")
	f_out= open('final_datasets/improved-person-data-v2.tsv','w+',encoding="utf8")

	#Copy Column Header
	f_out.write(f_in.readline())
	for line in f_in:
		# Read each line of the category improved dataset
		splits=line.strip().split('\t')
		splits = list( x.strip() for x in splits)
		
		uri=splits[0]
		gender=splits[3]
		f_out.write(splits[0])
		for i in range(1,len(splits)):
			if i==3:
				if dataset_lookup.get(uri)!=None:
					# In case the gender lookup has data
					# (Always take this data if available)
					f_out.write('\t'+dataset_lookup.get(uri))
				elif gender=='"male"@en':
					# Normalize
					f_out.write('\tmale')
				elif gender=='"female"@en':
					# Normalize
					f_out.write('\tfemale')
				else:
					# If there is still no data, write NA
					f_out.write('\tNA')
			else:
				f_out.write('\t'+splits[i])
		f_out.write('\n')

	f_in.close()
	f_out.close()

	print("improve_person_dataset_claudia - DONE")

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	improve_person_dataset_claudia()
