
import pandas as pd
import pickle
import datetime
import time
import os



master_data_path = 'politician-data'
profile_data_path = 'profile-data'
consolidated_path = 'edge-list'

master_data = pd.read_csv(master_data_path, sep='\t', encoding='utf-8')

if(not os.path.exists(consolidated_path)):
    os.makedirs(consolidated_path)
    
dates = []
for year in range(2016, 2000, -1):
    for month in range(12,0,-1):
        dates.append({'year':year, 'month':month})
        
def update_edge_list(file_name, content):
    fp = open(file_name, 'a',encoding='utf-8')
    fp.write(content)
    fp.close()

#create the files for every year and month if not present
for date in dates:
    date_file_name = str(date['year']).zfill(4)+'_'+str(date['month']).zfill(2)+'.csv'
    date_path = os.path.join(consolidated_path, date_file_name)
    if(not os.path.exists(date_path)):
        update_edge_list(date_path, '')
        
#get all the profile files
profile_paths = os.listdir(profile_data_path)
j = 0
for path in profile_paths:
    temp_file_path = os.path.join(profile_data_path, path)
    fp = open(temp_file_path,'rb') # read mode specifies a proper encoding
    list_frame = pickle.load(fp)
    print(list_frame.keys())
    for key in list_frame.keys():
        print(list_frame[key])
        break
    if (j == 100):
        break
    j += 1
    break

'''
start_time = time.time()
idx = 0
big_idx = 0
for path in paths:
    list_frame = pickle.load(open(basepath + path, 'rb'))
    keylist = list(list_frame.keys())
    for key in keylist:
        parsedList = wiki.parse(list_frame[key]['*'])
        links = parsedList['links']
        link_list = []
        for link in links:
            link_list.append(link['*'])
        #print(link_list)
        date_year = key.split('-')
        #print(date_year)
        consolidated_data.loc[idx] = [path,int(date_year[0]), int(date_year[1]),link_list]
        idx += 1
    print(path)
    big_idx += 1
    if(big_idx == 2):
        break
end_time = time.time()
print('Execution time - ',(end_time - start_time)/60)

pickle.dump(consolidated_data, open('consolidated-profile','wb'))

'''
'''
for path in paths:
    list_frame = pickle.load(open(base_path +'/' + paths[10], 'rb'))
    keylist = list(list_frame.keys())
    for key in keylist:
        content = list_frame[key]['*']
        print(content)
        print('-----------------------------------')
        parsedList = wiki.parse(list_frame[key]['*'])
        links = parsedList['links']
        link_list = []
        for link in links:
            link_list.append(link['*'])
        print(link_list)
        break
    break
'''
#read_data = pickle.load(open('consolidated-profile','rb'))