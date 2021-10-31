import pandas as pd
from twarc.client2 import Twarc2
import re
from twarckeys import consumer_key, consumer_secret, access_token, access_token_secret
from dask import dataframe as df1

t = Twarc2(consumer_key, consumer_secret, access_token, access_token_secret)

def url_proportion(subset_size):
    tweets = df1.read_csv(tweets_fn, sep='\t', dtype={'tweet_id': 'object'})

    subset = tweets.sample(frac=0.1)
    tweet_ids = subset['tweet_id']

    hydrated_tweets = t.tweet_lookup(tweet_ids)

    tweet_cnt = 0
    urls = 0
    batch_cnt = 0
    for batch in hydrated_tweets:
        batch_cnt += 1
        print(batch_cnt)
        for tweet in batch['data']:
            if not tweet_cnt > subset_size:
                tweet_cnt += 1
                try:
                    if 'urls' in tweet['entities'].keys():
                        urls += 1
                except KeyError:
                    pass
    print(f'The number of hydrated tweets was {tweet_cnt}. Based off of this dataset, the proportion of tweets that contain URLs is {urls/tweet_cnt}')


# tweet.keys()
# dict_keys(['entities', 'id', 'lang', 'context_annotations', 'source', 'public_metrics', 'possibly_sensitive', 'reply_settings', 'created_at', 'text', 'author_id', 'conversation_id', 'referenced_tweets'])