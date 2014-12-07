import csv
import datetime
from moon_scripts.solar_data import load_solar_data

def load_all_data():
    moon_data = csv.reader(open("../moon_data/ny_moon_dates.csv"))
    next(moon_data) # ignore header
    result = dict()
    for d, m in moon_data:
        cd = datetime.datetime.strptime(d, "%Y %b %d  %H:%M")
        t = cd.strftime("%H:%M")
        fd = cd.strftime("%Y-%m-%d")
        result.setdefault(fd, {})
        result[fd]['moon_time'] = t
        result[fd]['moon_day'] = m[:-1]

    moon_phase = csv.reader(open("../moon_data/moon_phase.csv"))

    for d,x,y in moon_phase:
        cd = datetime.datetime.strptime(d, "%Y %b %d  %H:%M")
        fd = cd.strftime("%Y-%m-%d")
        result.setdefault(fd, {})
        result[fd]['phase'] = x
        result[fd]['t'] = y

    q = load_solar_data()
    for d,v in q.items():
       result.setdefault(d, {})
       for x, y in v.items():
           result[d][x] = y

    all_keys = set()

    for r in result.values():
        for k in r.keys():
            all_keys.add(k)

    for r in result.values():
        for k in all_keys:
            r.setdefault(k, '-')


    return result

