import sys
from collections import Counter

def get_prop_coverage_stats():

	prop_coverage=dict()
	person_coverage=dict()
	prevent_dup=dict()

	f_in = open('data_extracted/literals_final.txt','r', encoding="utf8")

	print('Start counting')
	for line in f_in:
		splits=line.split()
		person=splits[0]
		prop=splits[1]
		
		if prevent_dup.get(person)==None:
			prevent_dup[person]=set()
			prevent_dup.get(person).add(prop)
		elif prop in prevent_dup.get(person):
			continue
		else:
			prevent_dup.get(person).add(prop)

		if person_coverage.get(person)==None:
			person_coverage[person]=1
		else :
			person_coverage[person]=person_coverage.get(person)+1

		if prop_coverage.get(prop)==None:
			prop_coverage[prop]=1
		else :
			prop_coverage[prop]=prop_coverage.get(prop)+1
	f_in.close()
	print('Finished counting')

	amount_people=len(person_coverage)
	amount_props=len(prop_coverage)

	print('----------------------------------------------------')
	print('Amount of people: '+str(amount_people))
	print('Amount of unique properties: '+str(amount_props))
	print('----------------------------------------------------')

	most_common_props=Counter(prop_coverage).most_common(50)
	print('Properties that can be found on most biographies:')

	for (x,y) in most_common_props:
		print('%20s %-.2f' % (x,y*100/amount_people))

	#f_out = open('data_extracted/property_coverage.txt','w+', encoding="utf8")

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	get_prop_coverage_stats()