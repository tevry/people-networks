import sys
from collections import Counter

def get_person_data_stats():

	prop_coverage=dict()
	index_to_propname=dict()
	amount_props=0
	try:
		f_in = open('prop_selection.txt','r', encoding="utf8")
	except IOError:
		print('Please create prop_selection.txt')

	c=3
	prop_coverage[c]=0
	index_to_propname[c]='gender'
	c=4
	for line in f_in:
		prop_coverage[c]=0
		index_to_propname[c]=line.strip()
		c+=1
		amount_props+=1
	f_in.close()

	max_index=c-1

	print("Please enter:")
	print("1 - original data")
	print("2 - improved-person-data-v1 (category)")
	print("3 - improved-person-data-v2 (claudia)")
	print("4 - improved-person-data-v3 (nationality)")
	print("5 - final actor data")
	print("6 - final author data")
	print("7 - final politician data")
	print("8 - final scientist data")
	print("9 - final sportsmen data")
	dec=input("Input:\n")
	if dec=='1':
		f_in = open('data_extracted/person-data.tsv','r', encoding="utf8")
	elif dec=='2':
		f_in = open('data_extracted/improved-person-data-v1.tsv','r', encoding="utf8")
	elif dec=='3':
		f_in = open('final_datasets/improved-person-data-v2.tsv','r', encoding="utf8")
	elif dec=='4':
		f_in = open('final_datasets/improved-person-data-v3.tsv','r', encoding="utf8")
	elif dec=='5':
		f_in = open('final_datasets/actor-data.tsv','r', encoding="utf8")
	elif dec=='6':
		f_in = open('final_datasets/author-data.tsv','r', encoding="utf8")
	elif dec=='7':
		f_in = open('final_datasets/politician-data.tsv','r', encoding="utf8")
	elif dec=='8':
		f_in = open('final_datasets/scientist-data.tsv','r', encoding="utf8")
	elif dec=='9':
		f_in = open('final_datasets/sportsmen-data.tsv','r', encoding="utf8")
	else:
		return

	print('Start counting')
	amount_people=0
	people_overall=dict()
	f_in.readline()
	for line in f_in:
		splits=line.split('\t')

		# Assume a person has none of the categories assigned
		person_coverage=[]
		for i in range(0,max_index-1):
			person_coverage.append(False)

		for i in range(3,max_index+1):
			if splits[i].strip()!='NA':
				prop_coverage[i]+=1
				person_coverage[i-3]=True

		if people_overall.get(tuple(person_coverage))==None:
			people_overall[tuple(person_coverage)]=1
		else:
			people_overall[tuple(person_coverage)]+=1

		amount_people+=1

	f_in.close()
	print('Finished counting')

	print('----------------------------------------------------')
	print('Amount of people: '+str(amount_people))
	print('----------------------------------------------------')

	print('%20s | %10s | %-s' % ('Property Name','Percentage','Total Count'))
	for x,y in prop_coverage.items():
		print('%20s | %10.2f | %-d' % (index_to_propname.get(x),y*100/amount_people,y))

	#f_out = open('data_extracted/property_coverage.txt','w+', encoding="utf8")
	print('\n')

	print('----------------------------------------------------')
	print('People property coverage overall')
	print('----------------------------------------------------')

	print('%55s \t->\t %10s | %-s' % ('Available Properties','Percentage','Total Count'))
	print('-'*97)

	for (key,value) in Counter(people_overall).most_common(20):
		key_string=''
		for i in range(0,len(key)):
			if key[i]==True:
				key_string+= index_to_propname.get(i+3) + ' '

		print('%55s \t->\t %10.2f | %-d' % (key_string,value*100/amount_people,value))

	print('-'*97)
	selection=(False,True,True,False,True,True,False)
	selection_amount=0
	for (key,value) in Counter(people_overall).most_common(100):
		if  (all ( (not selection[i] or key[i]) for i in range(0,len(selection)))):
			selection_amount+=value
	print('People that got at least: name + birthDate + occupation + nationality: '+ str(selection_amount))


if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	get_person_data_stats()