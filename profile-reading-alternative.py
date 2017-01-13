import pickle
import pandas as pd
from mwclient import Site
import datetime
import time
import os

from create_profile_reading_tracker import create_profile_reading_tracker


file_name = 'splits/politician-data-0-1000'
tracker_file = file_name+'-tracker.csv' # make sure the file is in parallel to this program

'''
to store the profile data. if the folder not present then it will create it
no path delimiters please. don't use // '''
base_path = 'profile-data' 

user_agent = 'Uni Koblenz-Landau student, marcelreif@uni-koblenz.de'
wiki = Site(host='en.wikipedia.org', clients_useragent=user_agent)

if(not os.path.exists(base_path)):
    os.makedirs(base_path)

#if the tracker file does not exists then create one
if not os.path.exists(tracker_file):
    create_profile_reading_tracker(file_name, tracker_file)

def read_profile_tracker() : 
    global profile_tracker
    profile_tracker = pd.read_csv(tracker_file,encoding="utf-8")
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

# Init date list (build backwards, because revisions are in backwards order as well)
# -> we are going back in time
dates = []
for year in range(2016,2000,-1):
    for month in range(12,0,-1):
        dates.append({'year':year, 'month':month})

while True:
    # get the profile to be read
    # read them completely
    #jump on to the next profile until everything is over
    start_profile_time = time.time()
    unread_profile = get_unread_profile(profile_tracker)
    if (unread_profile):

        # DEBUG
        # print("Start: "+unread_profile)

        # Init biography page and output dict
        profile_page = wiki.pages[unread_profile]
        profile_list = dict()

        # Get all revisions of the biography page
        # Revisions are ordered chronologically (starting with newest rev)
        timestamp_revisions = profile_page.revisions(prop='ids|timestamp')

        date_ind = 0 # Init on newest page
        relevant_ids = set() # Store all revisions that are needed (regarding our intervals)
        id_to_date_map = dict() # Used to remember all dates, where a page was online

        # This loop can be capsuled in a function for cleaner code
        for rev in timestamp_revisions:
            # go back in time and read all revisions

            # ID and Upload date of the webpage
            timestamp_id = rev['revid']
            timestamp = rev['timestamp']

            # DEBUG
            # print("---------------")
            # print("Next Revision: "+ str(timestamp.tm_mday) + " . " +str(timestamp.tm_mon)+ " . " + str(timestamp.tm_year))
            # print(str(dates[date_ind]["year"]) + " <= " + str(timestamp.tm_year) + " = " + str(dates[date_ind]["year"] <= timestamp.tm_year))
            # print(str(dates[date_ind]["year"]) + " == " + str(timestamp.tm_year) + " and " + str(dates[date_ind]["month"]) + " <= " + str(timestamp.tm_mon) + " = " + str((dates[date_ind]["year"] == timestamp.tm_year and dates[date_ind]["month"] <= timestamp.tm_mon)))

            if (dates[date_ind]["year"] < timestamp.tm_year) or (dates[date_ind]["year"] == timestamp.tm_year and dates[date_ind]["month"] <= timestamp.tm_mon):
                # If there are multiple revisions in a month skip these entries (the latest one in a per month will already be assigned by the loops)
                continue

            # Step after assignment, so you always have the latest version that was online on that date
            while (dates[date_ind]["year"] > timestamp.tm_year):
                # As long as the interval date year is bigger than the revision date (rev was there before interval date)
                # -> this revision was shown on all interval dates until then
                # -> we need to step with interval until you reach the point where the revision isn't the most recent one

                # DEBUG
                # print("Assigned to (year-filter): " +str(dates[date_ind]["month"]) +' . '+ str(dates[date_ind]["year"]))

                relevant_ids.add(timestamp_id)
                date_ind+=1

                # Build a list of all interval dates that this revision is assigned to
                if id_to_date_map.get(timestamp_id)==None:
                    id_to_date_map[timestamp_id]=[]
                id_to_date_map[timestamp_id].append(dates[date_ind])

            # Note: Years are equal at this point

            # Same as the "year adjustment loop" before -> adjust months
            while (dates[date_ind]["month"] > timestamp.tm_mon):
                
                # DEBUG
                # print("Assigned to (month-filter): " +str(dates[date_ind]["month"]) +' . '+ str(dates[date_ind]["year"]))

                relevant_ids.add(timestamp_id)
                date_ind+=1
                # Build a list of all dates that this revision is assigned to
                if id_to_date_map.get(timestamp_id)==None:
                    id_to_date_map[timestamp_id]=[]
                id_to_date_map[timestamp_id].append(dates[date_ind])
            # Months are equal at this point
            # END LOOP

        # DEBUG
        # print("Got Timestamps: " + str(relevant_ids))
        

        if len(relevant_ids)==0:
            # Catching case where someone moved the page (recently)
            # e.g. check "Bill_Malarky", it was the actual page until 3.1.2017, but was moved to "Bill_Malarkey_MHK"
            # -> the new "Bill_Makarky" only exists since 3.1.2017 which is out of our range, such that we get no revisions and ids
            # -> would break the algorithm -> SKIP AND DONT WRITE!
            profile_count += 1
            end_profile_time = time.time()
            print(profile_count,') '+unread_profile +' has changed!! No data retrieved '+'time taken(mins) - ',(end_profile_time - start_profile_time)/60)
            # Changed time taken in the output to "NA" so you can retrieve unmatched cases if desired
            write_read_profile(profile_tracker, unread_profile, "NA" )
            continue
            
        #look for article from the last minute of 1 st day of month.
        #Start from there and go back until you find a article which will give the state of article at that point
        relevant_revision_data = profile_page.revisions(list(relevant_ids) ,prop='ids|timestamp|extlinks')
        for article in relevant_revision_data:
            article_id = article['revid']
            # Assign the data of the article to all dates, where this page was online
            # NOTE: profile_list only contains data at the points in time, where the page already existed, if you try to fetch it use dict.get() so you will receive None and no error
            for date in id_to_date_map[article_id]:
                profile_list[str(date["year"])+'-'+str(date["month"])] = article
            break

        profile_count += 1
        end_profile_time = time.time()
        print(profile_count,') '+unread_profile +' is read. '+'time taken(mins) - ',(end_profile_time - start_profile_time)/60)
        
          
        # DEBUG - Comment the following lines if you dont want to write  

        # push the content to the file and update the tracker file  (this is done because even if program crashes - we will be able to resume)  
        pickle.dump(profile_list,open(base_path + '/'+unread_profile,'wb'))
        write_read_profile(profile_tracker, unread_profile, (end_profile_time - start_profile_time)/60 )

    else :
        print('Hooray!!!!!!! The job is over.')
        break

    # DEBUG - Only run one person
    # break

end_time = time.time()
print('Total Time taken (in mins)-',(end_time - start_time) / 60) 
print('No. of profiles read :',profile_count)


#profile_list
#unread_profile
#pickle.dump(profile_list,open('profile-data//'+unread_profile,'wb'))

