#!/usr/bin/env python3

'''
Functions for communicating with the CrowdTangle API via Python

Written by github.com/simonlindgren
'''

import requests
import time
import pandas as pd
import os
import glob

# create the data directory if it does not exist
if not os.path.exists('_data'):
    os.makedirs('_data')

def auth():
    global api_token
    api_token = input("Enter api token:\n")
    
def lists():
    params = {'token': api_token}
    resp = requests.get(f'https://api.crowdtangle.com/lists', params=params)
    if resp.status_code != 200:
    # This means something went wrong.
        print('GET /posts/search/ {}'.format(resp.status_code))
    lists_df = pd.DataFrame(resp.json()['result']['lists'])
    print(lists_df)
    
    global ids
    ids = lists_df.id.tolist()
    
def getlists(startdate,enddate,pause):
    params = {
    "count": '100',
    "sortBy": 'date',
    "startDate": startdate,
    "endDate": enddate,
    #"searchTerm": '', # we don't set any searchterm for within the lists
    "token": api_token
    #"listIds": "" # not setting this gets all Lists, but not Saved Searches
    }
    print("Getting data ...")
    resp = requests.get(f'https://api.crowdtangle.com/posts', params=params)
    
    if resp.status_code != 200:
        # This means something went wrong.
        print('GET /posts/ {}'.format(resp.status_code))
        pass
    
    filename = "_data/pyct-listdata-" + str(startdate) + "--" + str(enddate) + ".csv"
    
    # process data from first set of the query
    data = resp.json()
    data_df = pd.json_normalize(data['result']['posts'])
    data_df.to_csv(filename, index=False)
    
    # page for more data
    try:
        while 'nextPage' in data['result']['pagination']:
            next_page = data['result']['pagination']['nextPage']
            # print(f'Loading page ... {next_page}')
            print("Paging through results with " + next_page.split("&")[-1])
            resp = requests.get(next_page)
            if resp.status_code != 200:
                print('GET /posts/ {}'.format(resp.status_code))
                break
            data = resp.json()
            new_df = pd.json_normalize(data['result']['posts'])
            data_df = data_df.append(new_df, ignore_index=True)
            next_page = data['result']['pagination']['nextPage']

            # dump data to growing csv
            data_df.to_csv(filename, index=False)

            # go easy
            time.sleep(int(pause)) # sleep to avoid 429 error
    
    except Exception as e:
        data_df.to_csv(filename, index=False)
        counted = len(data_df)
        if counted > 9999:
            print("This time slice hit the limit of 10k posts, so you did not get all data. Try again with a narrower slice.")
        else:
            print("Done (" + str(len(data_df)) + " posts)")
            
def getsearch(listid,startdate,enddate,pause):
    params = {
    "count": '100',
    "sortBy": 'date',
    "startDate": startdate,
    "endDate": enddate,
    #"searchTerm": '', # we don't set any searchterm for within the lists
    "token": api_token,
    "listIds": [listid] # this chooses which Saved Search to retrieve data for
    }

    print("Getting data ...")
    resp = requests.get(f'https://api.crowdtangle.com/posts', params=params)
    
    if resp.status_code != 200:
        # This means something went wrong.
        print('GET /posts/ {}'.format(resp.status_code))
        pass
    
    filename = "_data/pyct-searchdata-" + str(listid) + "-" + "--" + str(enddate) + ".csv"
    
    # process data from first set of the query
    data = resp.json()
    data_df = pd.json_normalize(data['result']['posts'])
    counted = len(data_df)
    if counted == 0:
        print("This Saved Search list is empty.")
    else:
        pass
    data_df.to_csv(filename, index=False)
    
    # page for more data
    try:
        while 'nextPage' in data['result']['pagination']:
            next_page = data['result']['pagination']['nextPage']
            # print(f'Loading page ... {next_page}')
            print("Paging through results with " + next_page.split("&")[-1])
            resp = requests.get(next_page)
            if resp.status_code != 200:
                print('GET /posts/ {}'.format(resp.status_code))
                break
            data = resp.json()
            new_df = pd.json_normalize(data['result']['posts'])
            data_df = data_df.append(new_df, ignore_index=True)
            next_page = data['result']['pagination']['nextPage']

            # dump data to growing csv
            data_df.to_csv(filename, index=False)

            # go easy
            time.sleep(int(pause)) # sleep to avoid 429 error
    
    except Exception as e:
        data_df.to_csv(filename, index=False)
        counted = len(data_df)
        if counted > 9999:
            print("This time slice hit the limit of 10k posts, so you did not get all data. Try again with a narrower slice.")
        else:
            print("Done (" + str(len(data_df)) + " posts)")
            
    print("Totally done (" + str(len(data_df)) + " posts)")   
    
def getlistsfast(pause):
    params = {
    "count": '10000',
    "sortBy": 'date',
    "startDate": '',
    "endDate": '',
    #"searchTerm": '', # we don't set any searchterm for within the lists
    "token": api_token
    #"listIds": "" # not setting this gets all Lists, but not Saved Searches
    }
    
    print("Getting first batch ...")
    
    resp = requests.get(f'https://api.crowdtangle.com/posts', params=params)
    
    if resp.status_code != 200:
        # This means something went wrong.
        print('GET /posts/ {}'.format(resp.status_code))
        pass
    
    # process data from first set of the query
    data = resp.json()
    data_df = pd.json_normalize(data['result']['posts'])
    data_df.to_csv('_data/pyct-data-big.csv', index=False)
    
    
    print("Iterating for more data ...")
    
    # iterate for more data
    breakdate = data_df.date.tolist()[-1]
    print("Now back at " + str(breakdate))
    
    while True:
        try:
            params = {
            "count": '10000',
            "sortBy": 'date',
            "endDate": breakdate,
            "token": api_token
            }

            resp = requests.get(f'https://api.crowdtangle.com/posts', params=params)

            if resp.status_code != 200:
                # This means something went wrong.
                print('GET /posts/ {}'.format(resp.status_code))
                pass

            # process data from first set of the query
            data = resp.json()

            new_df = pd.json_normalize(data['result']['posts'], errors = 'ignore')
            data_df = data_df.append(new_df, ignore_index=True)

            data_df.to_csv('_data/pyct-data-big.csv', index=False)

            counted = len(data_df)
            print(str(counted) + " posts")
            breakdate = data_df.date.tolist()[-1]
            print("Now back at " + str(breakdate))
        
        except:
            pass

        # go easy
        time.sleep(int(pause)) # sleep to avoid 429 error
    
    print("Totally done (" + str(len(data_df)) + " posts)")
        
def search(count,startdate,enddate,sort_by,pause,searchterms):

    params = {
        "count": count,
        "sortBy": sort_by,
        "startDate": startdate,
        "endDate": enddate,
        "searchTerm": searchterms,
        "token": api_token
    }
    
    print("Searching ...")

    resp = requests.get(f'https://api.crowdtangle.com/posts/search', params=params)
    if resp.status_code != 200:
        # This means something went wrong.
        print('GET /posts/search/ {}'.format(resp.status_code))
    
    print("Getting first batch ...")
    
    resp = requests.get(f'https://api.crowdtangle.com/posts', params=params)
    
    if resp.status_code != 200:
        # This means something went wrong.
        print('GET /posts/ {}'.format(resp.status_code))
        pass
    
    # process data from first set of the query
    data = resp.json()
    data_df = pd.json_normalize(data['result']['posts'])
    data_df.to_csv('_data/pyct-data-search-' + str(enddate) + '.csv', index=False)
  
    # iterate for more data
    breakdate = list(data_df.date)[-1]
    print("This took us back to --> " + str(breakdate))
    print("Getting "  + str(count) + " more posts ...")
        
    while True:
        params = {
            "count": count,
            "sortBy": sort_by,
            "startDate": startdate,
            "endDate": breakdate,
            "searchTerm": searchterms,
            "token": api_token
        }
        
        resp = requests.get(f'https://api.crowdtangle.com/posts/search', params=params)
        
        if resp.status_code != 200:
            # This means something went wrong.
            print('GET /posts/search/ {}'.format(resp.status_code))

        # process this batch of data
        data = resp.json()
        data_df = pd.json_normalize(data['result']['posts'])
        data_df.to_csv('_data/pyct-data-search-' + str(breakdate) + '.csv', index=False)
        breakdate = list(data_df.date)[-1]
        print("Now at " + str(breakdate))
        
        # go easy
        time.sleep(int(pause)) # sleep to avoid 429 error
    
    print("Done (" + str(len(data_df)) + " posts)")
    
    
def joinsearchcsvs():
    filestomerge = [f for f in glob.glob("_data/pyct-data-search-*")]
    #combine all files in the list
    combined_df = pd.concat([pd.read_csv(f, low_memory=False) for f in filestomerge])
    #export to csv
    combined_df.to_csv("_data/pyct-data-search-all.csv", index=False, encoding='utf-8-sig')