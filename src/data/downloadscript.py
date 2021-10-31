import pandas as pd
import re
import twarckeys
import gzip
import datetime
import wget
import shutil
import os

def download_dailies(date, end_date):

    while date != end_date:
        str_date = date.strftime("%Y-%m-%d")
        dataset_url = f'https://github.com/thepanacealab/covid19_twitter/raw/master/dailies/{str_date}/{str_date}-dataset.tsv.gz'

        wget.download(dataset_url, out='dataset.tsv.gz')
        with gzip.open('dataset.tsv.gz', 'rb') as f_in:
            with open('dataset.tsv', 'ab') as f_out:
                shutil.copyfileobj(f_in, f_out)

        date += datetime.timedelta(days=1)

        os.unlink("dataset.tsv.gz")