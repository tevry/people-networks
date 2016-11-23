import sys
from collections import Counter

def get_persons_with_full_coverage():

	
	f_in = open('data_extracted/final-person-data.tsv','r', encoding="utf8")
	f_out = open('data_extracted/full_cov_demo.tsv','w+', encoding="utf8")

	c=0
	for line in f_in:
		splits=line.split('\t')

		complete=True
		for split in splits:
			if split.strip()=='NA':
				complete=False

		if complete==True:
			f_out.write(line)
			c+=1

		if c==20:
			break

	f_in.close()
	f_out.close()

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	get_persons_with_full_coverage()