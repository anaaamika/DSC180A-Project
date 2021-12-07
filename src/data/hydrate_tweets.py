from twarc.client2 import Twarc2
from twarckeys import consumer_key, consumer_secret, access_token, access_token_secret
from dask import dataframe as df1
import jsonlines

t = Twarc2(consumer_key, consumer_secret, access_token, access_token_secret)
subset_size = 2000000

def fetch_tweets(subset_size, tweets_ids_fn, tweets_fn):
    tweets = df1.read_csv(tweets_ids_fn, sep='\t', dtype={'tweet_id': 'object'})

    subset = tweets.sample(frac=0.1)
    tweet_ids = subset['tweet_id']

    hydrated_tweets = t.tweet_lookup(tweet_ids)

    tweet_cnt = 0
    for batch in hydrated_tweets:
        if tweet_cnt < subset_size:
            for tweet in batch['data']:
                if tweet_cnt < subset_size:
                    tweet_cnt += 1
                    with jsonlines.open(tweets_fn, 'a') as writer:
                        writer.write(tweet)
                else:
                    break
        else:
            break
    return

def missingness(tweet_ids_fn, outfolder='data'):
    t = Twarc2(consumer_key, consumer_secret, access_token, access_token_secret)
    
    num_samples = 100
    missing = []
    tweets = df1.read_csv(tweet_ids_fn, sep='\t', dtype={'tweet_id': 'object'})
    for i in range(num_samples):
        subset = tweets.sample(frac=0.1)
        tweet_ids = subset['tweet_id']
        
        hydrated_tweets = t.tweet_lookup(tweet_ids)
        tweet_cnt = 0
        for batch in hydrated_tweets:
                tweet_cnt += len(batch['data'])
        missing_prop = tweet_cnt / len(tweet_ids)
        missing.append(missing_prop)
        
        missing_interval = st.norm.interval(alpha=0.95, loc=np.mean(missing), scale=st.sem(missing))
        
    with open(outfolder + "/outputs.txt", "a") as text_file:
        text_file.write(f'The 95% confidence interval for the proportion of missing tweets is {missing_interva}.\n')
    print(missing)
    return
