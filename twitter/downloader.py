#! /usr/bin/env python2

import csv
import json
import time
import datetime
import requests
import urlparse
import dateutil.parser


API_URL = 'http://wefeel.csiro.au/api/'
TIMEPOINTS_URL = urlparse.urljoin(API_URL, 'emotions/primary/timepoints')


def get_unix_time(y, m, d):
    t = datetime.datetime(y, m, d)
    return int(time.mktime(t.timetuple()) * 1000)


def reformat_time(time_str):
    return dateutil.parser.parse(time_str).strftime('%Y-%m-%d')


def load_data():
    params = {'granularity': 'day', 'count': 'allNoRT',
              'continent': 'northAmerica', 'timezone': 'eastern',
              'start': str(get_unix_time(2014, 5, 1)),
              'end': str(get_unix_time(2014, 11, 30))}
    return requests.get(TIMEPOINTS_URL, params=params).json()


def write_csv(data):
    emotions = ['love', 'joy', 'sadness', 'other', 'anger', 'surprise',
                'fear', '*']
    with open('eastern.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['date'] + emotions)
        for d in data:
            writer.writerow([reformat_time(d['localStart']['start'])] +
                            [d['counts'][e] for e in emotions])


if __name__ == '__main__':
    write_csv(load_data())
