import csv
from os import listdir
from os.path import isfile, join, exists
from subprocess import call

LINK = 'http://rredc.nrel.gov/solar/old_data/nsrdb/1991-2010/targzs/744860.tar.gz'

def load_solar_data():
    path_to_files = "../data/solar"

    if not exists(path_to_files):
        call(["wget", LINK, '-O', 'solar.tar.gz'])
        call(["tar", "zxvf", 'solar.tar.gz'])
        call(["mv", "744860", "../data/solar"])
        call(["rm", "solar.tar.gz"])

    files = sum([list(open(path_to_files + "/" + f).readlines())[2:] for f in listdir(path_to_files) if isfile(join(path_to_files,f)) ], [])

    reader = list(csv.reader(files, delimiter=','))[2:]

    # ETR (W/m^2), Precip (cm)
    chosen_columns = {'ETR': 4, 'precip': 33}
    grouped_by = dict()

    for row in reader:
        if row[0] not in grouped_by:
            grouped_by[row[0]] = []
        grouped_by[row[0]].append(dict(map(lambda x: (x, row[chosen_columns[x]]), chosen_columns.keys())))


    result = dict()

    for k, v in grouped_by.items():
        result[k] = dict()

        for name in chosen_columns.keys():
            result[k][name] = int(sum(map(lambda i: float(i[name]), v)) / len(v))

    return result

if __name__ == '__main__':
    qq = load_solar_data()
    for l in qq.items():
        print(l)
    print(len(qq))
