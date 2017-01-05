
import pandas as pd
from mwclient import Site
import pickle
import datetime
import time
import os
import numpy as np

base_path = 'profile-data'

ua = 'Uni Koblenz-Landau student, kandhasamy@uni-koblenz.de'
wiki = Site(host='en.wikipedia.org', clients_useragent=ua)

#get all the profile files
paths = os.listdir(base_path)

# create a dataframe to hold all the profile data
#page - profile name, year and month. links_to - list of profile names which have links
consolidated_data = pd.DataFrame(columns=['page', 'year', 'month', 'links_to'])
consolidated_data.astype({'page':np.str, 'year':np.int32,'month':np.int32})

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

#read_data = pickle.load(open('consolidated-profile','rb'))