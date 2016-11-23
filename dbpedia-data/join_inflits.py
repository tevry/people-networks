#####################################
# join_inflits

# Input:	infobj_transformed(inflit).txt
#			filtered_inflit.txt

# Output:	literals_final.txt (joined list of literals, contains all literals used later)

# Description:
# Join the original infobox literal list with the extracted literals from the infobox objects
#####################################

import sys
import string

def join_inflits():

	f_in = open('data_extracted/filtered_inflit.txt','r', encoding="utf8")
	f_out = open('data_extracted/literals_final.txt','w+', encoding="utf8")

	print('Start processing: filtered_inflit.txt')
	for line in f_in:
		splits=line.split()
		subject=splits[0][1:-1]
		relation = splits[1].split("/")[-1][:-1]
		literal = ' '.join([x.lower().replace("\t"," ").replace(".","").replace(",","") for x in splits[2:]])
		literal = literal.split('^^')[0]
		f_out.write(subject + "\t" +relation+ "\t"+literal+"\n")		
	f_in.close()
	print('Finished: filtered_inflit.txt')

	print('Start processing: infobj_transformed(inflit).txt')
	f_in = open('data_extracted/infobj_transformed(inflit).txt','r', encoding="utf8")
	for line in f_in:
		splits=line.split()
		subject=splits[0][1:-1]
		relation = splits[1].split("/")[-1][:-1]
		literal = ' '.join([x.lower().replace("\t"," ").replace(".","").replace(",","") for x in splits[2:]])
		f_out.write(subject + "\t" +relation+ "\t"+literal+"\n")		
	f_in.close()
	print('Finished: infobj_transformed(inflit).txt')

	f_out.close()

	print('DONE!')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	join_inflits()