import sys
from collections import Counter

def get_link_data_stats():

	prop_coverage=dict()
	
	f_in=open('data_extracted/link-data.tsv','r',encoding='utf-8')

	print('Start counting')
	amount_links=0
	for line in f_in:
		splits=line.split()
		if(prop_coverage.get(splits[2])!=None):
			prop_coverage[splits[2]]+=1
		else:
			prop_coverage[splits[2]]=1
		amount_links+=1

	f_in.close()
	print('Finished counting')


	print('----------------------------------------------------')
	print('Amount of people: '+str(amount_links))
	print('----------------------------------------------------')

	print('%20s | %10s | %-s' % ('Connection Name','Percentage','Total Count'))
	for (x,y) in Counter(prop_coverage).most_common(20):
		print('%20s | %10.2f | %-d' % (x,y*100/amount_links,y))

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	get_link_data_stats()