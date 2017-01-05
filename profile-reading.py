
import pickle
import pandas as pd
from mwclient import Site
import datetime
import time
import os

from create_profile_reading_tracker import create_profile_reading_tracker


file_name = 'politician-data-100-200'
tracker_file = file_name+'-tracker.csv' # make sure the file is in parallel to this program

'''
to store the profile data. if the folder not present then it will create it
no path delimiters please. don't use // '''
base_path = 'profile-data' 

user_agent = 'Uni Koblenz-Landau student, kandhasamy@uni-koblenz.de'
wiki = Site(host='en.wikipedia.org', clients_useragent=user_agent)

if(not os.path.exists(base_path)):
    os.makedirs(base_path)

#if the tracker file does not exists then create one
if not os.path.exists(tracker_file):
    create_profile_reading_tracker(file_name, tracker_file)

def read_profile_tracker() : 
    global profile_tracker
    profile_tracker = pd.read_csv(tracker_file)
    profile_tracker = profile_tracker[['handle','finished_reading','time_taken_in_mins']]

def get_unread_profile(profile_tracker):
    data_to_be_read = profile_tracker[profile_tracker['finished_reading'] == False]
    if(data_to_be_read.shape[0] > 0) :
        return data_to_be_read.iloc[0]['handle']
    else:
        return None
    
def write_read_profile(profile_tracker, profile,time_taken):
    # this could be improved - rather than filtering two times - get the row handle and update it
    profile_tracker.loc[profile_tracker['handle'] == profile, 'finished_reading'] = True
    profile_tracker.loc[profile_tracker['handle'] == profile, 'time_taken_in_mins'] = time_taken 
    profile_tracker.to_csv(tracker_file)
    
start_time = time.time()
profile_count = 0
profile_tracker = None

read_profile_tracker()

while True:
    # get the profile to be read
    # read them completely
    #jump on to the next profile until everything is over
    start_profile_time = time.time()
    unread_profile = get_unread_profile(profile_tracker)
    if (unread_profile):
        profile_page = wiki.pages[unread_profile]
        profile_list = {}
        # go through all the years and all months and read a single article (or the latest previous article)
        for year in range(2001,2017):
            for mon in range(1,13):
                dateObj = datetime.date(year, mon, 1)
                #startDate = dateObj.isoformat()+'T00:00:00Z'
                endDate = dateObj.isoformat()+'T23:59:59Z'
                #look for article from the last minute of 1 st day of month.
                #Start from there and go back until you find a article which will give the state of article at that point
                for article in profile_page.revisions(start=endDate, prop='ids|timestamp|content',dir='older', limit=1):
                    profile_list[str(year)+'-'+str(mon)] = article
                    break
        profile_count += 1
        end_profile_time = time.time()
        print(profile_count,') '+unread_profile+' is read. '+'time taken(mins) - ',(end_profile_time - start_profile_time)/60)
        
        #push the content to the file and update the tracker file  (this is done because even if program crashes - we will be able to resume)      
        pickle.dump(profile_list,open(base_path + '/'+unread_profile,'wb'))
        write_read_profile(profile_tracker, unread_profile, (end_profile_time - start_profile_time)/60 )
    else :
        print('Hooray!!!!!!! The job is over.')
        break
end_time = time.time()
print('Total Time taken (in mins)-',(end_time - start_time) / 60) 
print('No. of profiles read :',profile_count)


#profile_list
#unread_profile
#pickle.dump(profile_list,open('profile-data//'+unread_profile,'wb'))

