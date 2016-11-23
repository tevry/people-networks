import json
import sys

def build_linkprop():

	f_in = open('data_extracted/infobj_transformed(links).txt','r', encoding="utf8")
	f_out = open('data_extracted/linkproperties_final.txt','w+', encoding="utf8")
	
	linkprop_assignment=dict()

	for line in f_in:
		splits=line.split()
		subject=splits[0][1:-1]
		linkprop=splits[1].split("/")[-1][:-1]
		subject2=splits[2][1:-1]

		f_out.write(subject + '\t' + subject2 + '\t' + linkprop + '\n')
		if linkprop_assignment.get(subject)==None:
			linkprop_assignment[subject]=dict()
			linkprop_assignment[subject][subject2]=[linkprop]
		else:
			if linkprop_assignment.get(subject).get(linkprop)==None:
				linkprop_assignment[subject][subject2]=[linkprop]
			else:
				linkprop_assignment[subject][subject2].append(linkprop)


	f_in.close()
	f_out.close()
	with open('data_extracted/linkprop_assignment.json','w+', encoding='utf8') as f_json:
		json.dump(linkprop_assignment, f_json, ensure_ascii=False)

	print('DONE!')

if __name__ == "__main__":
	if len(sys.argv)>1:
		raise IOError("Overspecified")
	build_linkprop()