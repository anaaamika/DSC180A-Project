#!/usr/bin/env python

import sys
import json
import os

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/analysis')
sys.path.insert(0, 'test')

from hydrate_tweets import fetch_tweets
from download_ids import download_tweet_ids
import eda
import generate_data

def main(targets):
    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)

        download_tweet_ids(**data_cfg["download_params"])
        fetch_tweets(**data_cfg["hydrate_params"])
        
    if 'analysis' in targets:
        with open('config/analysis-params.json') as fh:
            analysis_cfg = json.load(fh)

        eda.url_proportion(**analysis_cfg)

    if 'model' in targets:
        print("Coming soon!")
        
    if 'test' in targets:
        with open('config/test-params.json') as fh:
            test_cfg = json.load(fh)
        print('here')
        if not os.path.exists('test/testdata/test_tweets.jsonl') or os.path.getsize('test/testdata/test_tweets.jsonl') == 0:
            generate_data.create_test_data(test_cfg['num_tweets'])
            print('here')
            
        eda.url_proportion(**test_cfg)
            
    
    
if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
