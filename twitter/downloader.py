import csv
import time
import datetime
import requests
import urllib.parse
import dateutil.parser
from moon_scripts.merger import load_all_data


API_URL = 'http://wefeel.csiro.au/api/'
TIMEPOINTS_URL = urllib.parse.urljoin(API_URL, 'emotions/primary/timepoints')


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
    all_data = load_all_data()
    feature_keys = all_data.values()[0].keys()

    def format_features(d):
        r = []
        for k in feature_keys:
            if k in d:
                r.append(d[k])
            else:
                r.append('-')

        return r

    emotions = ['love', 'joy', 'sadness', 'other', 'anger', 'surprise',
                'fear', '*']
    with open('eastern.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['date'] + emotions + feature_keys)
        for d in data:
            fd = reformat_time(d['localStart']['start'])
            fs = all_data[fd] if fd in all_data else {}
            fs = format_features(fs)
            writer.writerow([fd] +
                            [d['counts'][e] for e in emotions] + fs)


if __name__ == '__main__':
    write_csv(load_data())
