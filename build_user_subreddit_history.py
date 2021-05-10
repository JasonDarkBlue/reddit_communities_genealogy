from datetime import datetime
import json, pickle
import timeit, random, lzma
import gzip, os, csv
from collections import defaultdict, Counter

def read_json_list(input_file):
    with gzip.open(input_file) if input_file.endswith(".gz") \
            else open(input_file) as fin:
        for line in fin:
            obj = json.loads(line)
            yield obj

def build_user_subreddit_history(subs = [], founders = 10, comments = False, ):
    author_sub_timestamps_dic = defaultdict(list)
    sub_author_timestamps_dic = defaultdict(list)
    sub_founders_dic = defaultdict(list)
    
    prefix = 'posts'
    if comments:
        prefix = 'comments'
    
    for sub in subs:
        filename = "data/{1}/{0}/{1}_jsonlists.gz".format(sub, prefix)
        for dic in read_json_list(filename):
            if 'subreddit' in dic:
                subreddit = dic['subreddit']
                created_time = dic['created_utc']
                author = dic['author']
                    
                if author != '[deleted]':
                    author_sub_timestamps_dic[author].append((subreddit, created_time))
                    sub_author_timestamps_dic[subreddit].append((author, created_time))
    
    # sorted based on created_time
    for author in author_sub_timestamps_dic:
        sub_timestamps_list = author_sub_timestamps_dic[author]
        sub_timestamps_list = sorted(sub_timestamps_list, key = lambda element : element[1])
        author_sub_timestamps_dic[author] = sub_timestamps_list
    
    for sub in sub_author_timestamps_dic:
        author_timestamps_list = sub_author_timestamps_dic[sub]
        author_timestamps_list = sorted(author_timestamps_list, key = lambda element : element[1])
        sub_author_timestamps_dic[subreddit] = author_timestamps_list
        
        author_set = set()
        
        for author, timestamp in author_timestamps_list:
            if author in author_set:
                continue
            sub_founders_dic[sub].append((author, timestamp))
            author_set.add(author)
    
    f = open("data/author_sub_timestamps_dic.pkl", "wb")
    pickle.dump(author_sub_timestamps_dic, f)
    f.close()
    
    f = open("data/sub_author_timestamps_dic.pkl", "wb")
    pickle.dump(sub_author_timestamps_dic, f)
    f.close()
    
    f = open("data/sub_founders_dic.pkl", "wb")
    pickle.dump(sub_founders_dic, f)
    f.close()
    
    return author_sub_timestamps_dic, sub_author_timestamps_dic, sub_founders_dic


