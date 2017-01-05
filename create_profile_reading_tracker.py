import pandas as pd

def create_profile_reading_tracker(file_name, tracker_file_name) :
    
    #read the given data file and extract all the profile names
    pol = pd.read_csv(file_name,sep='\t')
    handle_list = [x.split('/')[-1] for x in pol['WikiURL']]
    
    #create a data frame with handle, finish reading boolean and time taken columns
    handle_frame = pd.DataFrame(data=handle_list, columns=['handle'])
    handle_frame['finished_reading'] = False
    handle_frame['time_taken_in_mins'] = 0.0
    handle_frame.to_csv(tracker_file_name)
