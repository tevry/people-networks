import sys
from collections import Counter
import ast

def get_person_property_overview():

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
		print("Wrong Input")
		return

	print("\n\nWhich property should be reviewed?\n")
	firstLine = f_in.readline().strip().split("\t")
	for i in range(4,len(firstLine)):
		print(str(i-3) + " - "+firstLine[i])
	dec=input("Input:\n")

	if dec.isdigit() and int(dec)>0 and int(dec)<len(firstLine):
		col=int(dec)+3
	else:
		print("Wrong Input")
		return

	print('Start counting')
	counts = dict()
	
	amout_prop=0
	amount_people=0
	people_with_prop=0
	for line in f_in:
		value=line.strip().split('\t')[col]

		if value!='NA':
			people_with_prop+=1
			value=ast.literal_eval(value)
			amout_prop+=len(value)
			for element in value:
				if counts.get(element)!=None:
					counts[element]+=1
				else:
					counts[element]=1
		amount_people+=1

	f_in.close()
	print('Finished counting')

	print('----------------------------------------------------')
	print('Amount of people (total): '+str(amount_people))
	print('Amount of people (with property): '+str(people_with_prop))
	print('Amount of properties assigned (multiple per person): '+str(amout_prop))
	print('----------------------------------------------------')

	print('%30s \t->\t %10s | %10s | %-s' % ('Property Value','%','Relative %','Total Count'))
	print('-'*97)

	for (key,value) in Counter(counts).most_common(100):
		print('%30s \t->\t %10.2f | %10.2f | %-d' % ('"'+key+'"',value*100/amount_people,value*100/people_with_prop,value))

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	get_person_property_overview()