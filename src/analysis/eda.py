import json
from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as st
from twarc.client2 import Twarc2
from dask import dataframe as df1
import pandas as pd
import requests
import jsonlines
    
def url_proportion(num_tweets, tweets_fn, outfolder='data'):
    urls = 0
    retweets = 0
    users = {}
    with open(tweets_fn) as file:
        for line in file:
            tweet = json.loads(line)
            user_id = tweet['author_id']
            if user_id in users:
                users[user_id] += 1
            else:
                users[user_id] = 1
            try:
                if 'urls' in tweet['entities'].keys():
                    urls += 1
                if ('referenced_tweets' in tweet['entities'].keys()) or (tweet['text'][:2] == 'RT'):
                    retweets += 1

            except KeyError:
                pass
            
    url_prop = urls/int(num_tweets)
    retweet_prop = retweets/int(num_tweets)
    unique_users = len(users)
    
    with open(outfolder + "/outputs.txt", "w") as text_file:
        text_file.write(f'The proportion of tweets with urls was {url_prop}.\n')
        text_file.write(f'The proportion of retweets was {retweet_prop}.\n')
        text_file.write(f'The number of unique users was {unique_users}.\n')
    
    tweet_distribution = list(users.values())
    plt.hist(tweet_distribution, bins=[1, 2, 3, 4, 5])
    plt.savefig(outfolder + "/tweet_distribution_users.png", bbox_inches='tight')

def urls(tweets_fn, urls_fn, outfolder='data'):
    with open(tweets_fn) as file:
        for line in file:
            tweet = json.loads(line)
            try:
                if 'urls' in tweet['entities'].keys():
                    with jsonlines.open(urls_fn, 'a') as writer:
                        writer.write(tweet['entities']['urls'])
            except KeyError:
                pass
    return
    
def misinformation_proportion(urls_fn, misinformation_csv, outfolder='data'):
    num = 0
    misinformation = 0
    misinformation_sites = pd.read_csv(misinformation_csv)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46'}
    with open(urls_fn) as file:
        for line in file:
            num += 1
            url = json.loads(line)[0]['url']
            response = requests.get(url, headers=headers)
            if misinformation_sites['Domain'].str.contains(str(response.url), regex=False).any():
                misinformation += 1
    with open(outfolder + "/outputs.txt", "a") as text_file:
        text_file.write(f'The proportion of URLs leading to misinformation was {misinformation/num}.\n')
    return
