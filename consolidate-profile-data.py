
import pandas as pd
import pickle
import datetime
import time
import os


start_time = time.time()

master_data_path = 'politician-data'
profile_data_path = 'profile-data-full'
consolidated_path = 'edge-list'

# master data is required to convert the links to ID to store in edge list
master_data = pd.read_csv(master_data_path, sep='\t', encoding='utf-8')

# if consolidated path is not present then create it
if(not os.path.exists(consolidated_path)):
    os.makedirs(consolidated_path)
    
# create year, month pair which will be useful to create edge list for each pair
dates = []
for year in range(2016, 2000, -1):
    for month in range(12,0,-1):
        dates.append({'year':year, 'month':month})
     
# it appends the content to respective file
def update_edge_list(file_name, content):
    fp = open(file_name, 'a',encoding='utf-8')
    fp.write(content)
    fp.close()

#create the files for every year and month if not present
for date in dates:
    date_file_name = str(date['year']).zfill(4)+'_'+str(date['month']).zfill(2)+'.csv'
    date_path = os.path.join(consolidated_path, date_file_name)
    if(not os.path.exists(date_path)):
        update_edge_list(date_path, 'from,to\n')
        
# go through the master list and create a handle to ID dictionary
handle_list = [x.split('/')[-1] for x in master_data['WikiURL']]
id_list = [x for x in master_data['ID']]
handle_to_id = {}
for i in range(0, len(handle_list)):
    handle_to_id[handle_list[i]] = id_list[i]

print('No of IDs - ',len(handle_to_id))        

#get all the profile files
profile_paths = os.listdir(profile_data_path)
j = 0
# go through one by one and get the data
# go through all the keys which is a combination of year and month
# In each key get the list of links and convert each one of them into IDs from master data
# write the IDs by converting them into sparse notation into each respective file (year and month)

for path in profile_paths:
    temp_file_path = os.path.join(profile_data_path, path)
    fp = open(temp_file_path,'rb') # read mode specifies a proper encoding
    list_frame = pickle.load(fp)
    #print(list_frame.keys())
    for key in list_frame:
        #print(list_frame[key]['*'])
        temp_data = ''
        for link in list_frame[key]['*']:
            if(link in handle_to_id.keys()):
                temp_data += path+','+str(handle_to_id[link])+'\n'
        date_path = os.path.join(consolidated_path, key+'.csv')
        if(temp_data != ''):
            #print('Updating - ',date_path)
            update_edge_list(date_path, temp_data)
    #if (j == 100):
    #    break
    j += 1
    print('File - ',path,' is over')
    
end_time = time.time()

print('Total time taken(in sec) - ',(end_time-start_time))

