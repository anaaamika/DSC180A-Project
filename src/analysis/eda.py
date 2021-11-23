import json
from matplotlib import pyplot as plt

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
                if 'referenced_tweets' in tweet['entities'].keys():
                    retweets += 1

            except KeyError:
                pass
            
    url_prop = urls/int(num_tweets)
    retweet_prop = retweets/int(num_tweets)
    unique_users = len(users)
    
    with open(outfolder + "/outputs.txt", "a") as text_file:
        text_file.write(f'The proportion of tweets with urls was {url_prop}.\n')
        text_file.write(f'The proportion of retweets was {retweet_prop}.\n')
        text_file.write(f'The number of unique users was {unique_users}.\n')
   
    
    tweet_distribution = list(users.values())
    plt.hist(tweet_distribution, 20)
    plt.savefig(outfolder + "/tweet_distribution_users.png", bbox_inches='tight')
    
def misinformation_proportion():
    return
