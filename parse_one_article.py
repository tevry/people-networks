import pickle
import pandas as pd
from mwclient import Site
import datetime
import time
import os
import wikitextparser as wtp
import sys
import csv
from memory_profiler import profile
import gc
fp=open('memory_profiler2.log','w+')

@profile(stream=fp)
def parse_one_article(unread_profile,dates,ind,base_path,parsed_tracker,profile_count,wiki):
    start_profile_time = time.time()
    # Init biography page and output dict
    profile_page = wiki.pages[unread_profile[0]]
    profile_list = dict()
    
    # Get all revisions of the biography page
    # Revisions are ordered chronologically (starting with newest rev)
    timestamp_revisions = profile_page.revisions(prop='ids|timestamp')
    
    date_ind = 0 # Init on newest page
    relevant_ids = set() # Store all revisions that are needed (regarding our intervals)
    id_to_date_map = dict() # Used to remember all dates, where a page was online
    
    for rev in timestamp_revisions:
        # go back in time and read all revisions

        # ID and Upload date of the webpage
        timestamp_id = rev['revid']
        timestamp = rev['timestamp']
        
        if (dates[date_ind]["year"] < timestamp.tm_year) or (dates[date_ind]["year"] == timestamp.tm_year and dates[date_ind]["month"] <= timestamp.tm_mon):
            # If there are multiple revisions in a month skip these entries (the latest one in a per month will already be assigned by the loops)
            continue
        
        while (dates[date_ind]["year"] > timestamp.tm_year):
            # As long as the interval date year is bigger than the revision date (rev was there before interval date)
            # -> this revision was shown on all interval dates until then
            # -> we need to step with interval until you reach the point where the revision isn't the most recent one

            # DEBUG
            # print("Assigned to (year-filter): " +str(dates[date_ind]["month"]) +' . '+ str(dates[date_ind]["year"]))

            relevant_ids.add(timestamp_id)
            # Build a list of all interval dates that this revision is assigned to
            if id_to_date_map.get(timestamp_id)==None:
                id_to_date_map[timestamp_id]=[]
            id_to_date_map[timestamp_id].append(dates[date_ind])
            # Move Interval border
            date_ind+=1
        while (dates[date_ind]["month"] > timestamp.tm_mon):
            
            # DEBUG
            # print("Assigned to (month-filter): " +str(dates[date_ind]["month"]) +' . '+ str(dates[date_ind]["year"]))

            relevant_ids.add(timestamp_id)
            
            # Build a list of all interval dates that this revision is assigned to
            if id_to_date_map.get(timestamp_id)==None:
                id_to_date_map[timestamp_id]=[]
            id_to_date_map[timestamp_id].append(dates[date_ind])
            # Move Interval border
            date_ind+=1
            
    if len(relevant_ids)==0:
        # Catching case where someone moved the page (recently)
        # e.g. check "Bill_Malarky", it was the actual page until 3.1.2017, but was moved to "Bill_Malarkey_MHK"
        # -> the new "Bill_Makarky" only exists since 3.1.2017 which is out of our range, such that we get no revisions and ids
        # -> would break the algorithm -> SKIP AND DONT WRITE!
        #profile_count += 1
        end_profile_time = time.time()
        print(ind,') '+unread_profile[0] +' has changed!! No data retrieved '+'time taken(mins) - ',(end_profile_time - start_profile_time)/60)
        # Changed time taken in the output to "NA" so you can retrieve unmatched cases if desired
        #write_read_profile(profile_tracker, unread_profile[0], 0) #"NA" )
        
        parsed_articles = open(parsed_tracker,'a')
        pw = csv.writer(parsed_articles,lineterminator='\n') #Csv writer
        pw.writerows([[ind,unread_profile[0],unread_profile[1],True,0]]) #Writing down info about parsed file
        parsed_articles.close()
        return


    list_rel_ids = list(relevant_ids)
    chunks = []
    upper = 50
    lower = 0
    
    while (lower < len(relevant_ids)):
        chunks.append(list_rel_ids[lower:upper])
        lower = upper
        upper += 50

    count = 0
    for chunk in chunks:
        relevant_revision_data = wiki.revisions( chunk ,prop='ids|timestamp|content')
        for article in relevant_revision_data:
            count+=1
            article_id = article['revid']
            if('*' in article.keys()):
                # convert the content into wiki links and store only that
                wt = wtp.parse(article['*'])
                # replace the space with under_score and the rest seems to fine
                # commas are also present in URL
                temp_links = [wi.target.replace(' ','_') for wi in wt.wikilinks]
                #duplicate links are removed
                article['*'] = list(set(temp_links))
            else:
                print(article_id)
                article['*'] = []
            # Assign the data of the article to all dates, where this page was online
            # NOTE: profile_list only contains data at the points in time, where the page already existed, if you try to fetch it use dict.get() so you will receive None and no error
            for date in id_to_date_map[article_id]:
                temp = str(date["year"]).zfill(4)+'_'+str(date["month"]).zfill(2)
                profile_list[temp] = article
            del article
        del relevant_revision_data
        del chunk
    #profile_count += 1
    end_profile_time = time.time()
    print(profile_count,') ('+str(ind)+') '+unread_profile[0] +' is read. '+'time taken(mins) - ',(end_profile_time - start_profile_time)/60)
    pickle.dump(profile_list,open(base_path + '/'+str(unread_profile[1]),'wb'))
    #write_read_profile(profile_tracker, unread_profile[0], (end_profile_time - start_profile_time)/60 )
    parsed_articles = open(parsed_tracker,'a')
    pw = csv.writer(parsed_articles,lineterminator='\n') #Csv writer
    pw.writerows([[ind,unread_profile[0],unread_profile[1],True,(end_profile_time - start_profile_time)/60 ]]) #Writing down info about parsed file
    parsed_articles.close()
    
    del chunks
    del wiki
    gc.collect()
    return 