import io
import csv
import requests
import dateutil.parser
from moon_scripts.merger import load_all_data


WEATHER_URL = 'http://www.wunderground.com/history/airport/LBSF/{0}/1/1/CustomHistory.html?dayend=31&monthend=12&yearend={0}&req_city=NA&req_state=NA&req_statename=NA&format=1'


def load_raw_year(y):
    return requests.get(WEATHER_URL.format(y))


def load_year_table(y):
    sf = io.StringIO(load_raw_year(y).text.replace('<br />', ''))
    t = list(csv.reader(sf))[1:]
    t[0][0] = 'date'
    return t


def load_all(fy, ly, fn):
    all_data = load_all_data()
    feature_keys = list(all_data.values())[0].keys()

    def format_features(d):
        r = []
        for k in feature_keys:
            if k in d:
                r.append(d[k])
            else:
                r.append('-')
        return r

    def add_moon(row):
        fd = dateutil.parser.parse(row[0]).strftime('%Y-%m-%d')
        fs = all_data[fd] if fd in all_data else {}
        fs = format_features(fs)
        return row + fs

    with open(fn, 'w') as f:
        writer = csv.writer(f)
        ft = load_year_table(fy)
        writer.writerow(ft[0] + list(feature_keys))
        writer.writerows(map(add_moon, ft[1:]))
        for y in range(fy + 1, ly + 1):
            writer.writerows(map(add_moon, load_year_table(fy)[1:]))


if __name__ == '__main__':
    load_all(2004, 2014, 'sofia.csv')
