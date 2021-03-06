import csv
import datetime
from moon_scripts.sofia import load_data_as_dict
from moon_scripts.solar_data import load_solar_data
from moon_scripts.noaa_parser import load_noaa_data
from moon_scripts.aviation import load_aviation_as_dict
import os
from itertools import dropwhile

def load_all_data():
    moon_data = csv.reader(open("../moon_data/ny_moon_dates.csv"))
    next(moon_data) # ignore header
    result = dict()
    for d, m in moon_data:
        cd = datetime.datetime.strptime(d, "%Y %b %d  %H:%M")
        cd += datetime.timedelta(hours=12)
        t = cd.strftime("%H:%M")
        fd = cd.strftime("%Y-%m-%d")
        result.setdefault(fd, {})
        #result[fd]['moon_time'] = t
        result[fd]['moon_day'] = m[:-1]

    moon_phase = csv.reader(open("../moon_data/moon_phase.csv"))

    for d,x,y in moon_phase:
        cd = datetime.datetime.strptime(d, "%Y %b %d  %H:%M")
        fd = cd.strftime("%Y-%m-%d")
        result.setdefault(fd, {})
        result[fd]['phase'] = x
        #result[fd]['t'] = y

    #q = load_solar_data()
    #for d,v in q.items():
    #   result.setdefault(d, {})
    #   for x, y in v.items():
    #       result[d][x] = y

    q = load_noaa_data()
    for d,v in q.items():
        result.setdefault(d, {})
        for x, y in v.items():
            result[d][x] = y

    ## planets
    for planet in os.listdir("../planets"):
        with open("../planets/" + planet) as file:
            for line in file:
                if line.startswith('$$SOE'):
                    break
            reader = csv.reader(file)
            for d in reader:
                if (d[0].startswith('$$EOE')):
                    break
                splitted = d[0].split()
                cd = datetime.datetime.strptime(splitted[0], "%Y-%b-%d")
                fd = cd.strftime("%Y-%m-%d")
                if fd in result:
                    result[fd][planet[:-4]] = float(splitted[-1])


    all_keys = set()

    for r in result.values():
        for k in r.keys():
            all_keys.add(k)

    for r in result.values():
        for k in all_keys:
            if k == 'phase':
                r.setdefault(k, 'O')
            else:
                r.setdefault(k, '-')


    return result


def merge_with(estimated, name):
    data = load_all_data()
    result = dict()
    for k in estimated.keys():
        if k in data:
            result[k] = data[k]
            result[k][name] = estimated[k]

    return result


def print_csv(data, filename):
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        dates = sorted(data.keys())
        names = [""] + ["date"] +  (data.values()[0]).keys()
        names = map(lambda x: "%s" % (str(x),), names)
        writer.writerow(list(names))
        counter = 0
        for date in dates:
            counter += 1
            writer.writerow([counter, date] + data[date].values())

if __name__ == '__main__':
    print_csv(merge_with(load_data_as_dict(), 'accidents'), '../data/accidents.csv')
    print_csv(merge_with(load_aviation_as_dict(), 'aviation'), '../data/AviationDates.csv')
