import pickle
import pandas as pd
from mwclient import Site
import datetime
import time
import os
import wikitextparser as wtp
import sys
import csv

from create_profile_reading_tracker import create_profile_reading_tracker


#prev_size = 1 #DEBUG checking the size of dict


file_name = 'politician-data'
tracker_file = file_name+'-tracker.csv' # make sure the file is in parallel to this program
parsed_tracker = 'parsed_articles.csv'
'''
to store the profile data. if the folder not present then it will create it
no path delimiters please. don't use // '''
base_path = 'profile-data' 

user_agent = 'Uni Koblenz-Landau student, vasilev@uni-koblenz.de'
wiki = Site(host='en.wikipedia.org', clients_useragent=user_agent)

if(not os.path.exists(base_path)):
    os.makedirs(base_path)

    
#if the tracker file does not exists then create one
if not os.path.exists(tracker_file):
    create_profile_reading_tracker(file_name, tracker_file)

if not os.path.exists(parsed_tracker):
    parsed_articles = open(parsed_tracker,'w')
    pw = csv.writer(parsed_articles,lineterminator='\n') #Csv writer
    pw.writerows([['ind','handle','ID','finished_reading','time_taken_in_mins']]) # Writing column names
    parsed_articles.close()

#parsed_articles = open(parsed_tracker,'w') #Opening csv file to store information about parsed articles
#pw = csv.writer(parsed_articles) #Csv writer
#pw.writerows([,'handle','ID','finished_reading','time_taken_in_mins']) # Writing column names    

def read_profile_tracker() : 
    global profile_tracker
    profile_tracker = pd.read_csv(tracker_file,encoding='ISO-8859-1')
    profile_tracker = profile_tracker[['handle','ID']]#,'finished_reading','time_taken_in_mins']]
    ptr = pd.read_csv(parsed_tracker,encoding='ISO-8859-1',index_col='ind')
    profile_tracker = profile_tracker.iloc[ptr.shape[0]:]
    
"""
def get_unread_profile(profile_tracker):
    data_to_be_read = profile_tracker[profile_tracker['finished_reading'] == False]
    if(data_to_be_read.shape[0] > 0) :
        #returns the name and ID
        return [data_to_be_read.iloc[0]['handle'],data_to_be_read.iloc[0]['ID']]
    else:
        return None
    
def write_read_profile(profile_tracker, profile,time_taken):
    # this could be improved - rather than filtering two times - get the row handle and update it
    pt = profile_tracker[profile_tracker['handle'] == profile]#.index[0]
    #profile_tracker.set_value(ptindex, 'finished_reading', True)
    #profile_tracker.set_value(ptindex, 'time_taken_in_mins', time_taken)
    #profile_tracker.loc[profile_tracker['handle'] == profile, 'finished_reading'] = True
    #profile_tracker.loc[profile_tracker['handle'] == profile, 'time_taken_in_mins'] = time_taken 
    #profile_tracker.to_csv(tracker_file)
    parsed_articles = open(parsed_tracker,'a')
    pw = csv.writer(parsed_articles) #Csv writer
    pw.writerows([pt.index[0],profile,ptiloc[0,1],True,time_taken]) #Writing down info about parsed file
    parsed_articles.close()
"""    
    
start_time = time.time()
profile_count = 0
profile_tracker = None

read_profile_tracker()


# Init date list (build backwards, because revisions are in backwards order as well)
# -> we are going back in time
dates = []
for year in range(2016,2000,-1):
    for month in range(12,0,-1):
        dates.append({'year':year, 'month':month})
from parse_one_article import parse_one_article
for ind, row in profile_tracker.iterrows():
    profile_count += 1
    unread_profile = [row['handle'],row['ID']]
    # Init biography page and output dict
    parse_one_article(unread_profile,dates,ind,base_path,parsed_tracker,profile_count)

end_time = time.time()
print('Total Time taken (in mins)-',(end_time - start_time) / 60) 
print('No. of profiles read :',profile_count)    