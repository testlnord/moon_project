import csv
from os import listdir
from os.path import isfile, join, exists
import re
from subprocess import call

LINK = 'http://rredc.nrel.gov/solar/old_data/nsrdb/1991-2010/targzs/744860.tar.gz'

def parse_dst(result):
    path_to_files = "../data/dst"
    if not exists(path_to_files):
        call(["mkdir", path_to_files])
        for y in range(2011, 2015):
            for m in range(1, 13):
                call([
                    "wget",
                    "http://www.aer.com/sites/default/files/Dst_%d_%02d.txt" % (y, m),
                    "-O", path_to_files + "/" + "%d_%02d.txt" % (y,m)
                ])

    files = sum([list(open(path_to_files + "/" + f).readlines())[2:] for f in listdir(path_to_files) if isfile(join(path_to_files,f)) ], [])
    files = filter(lambda x: re.match("\s+\d+-\d+-\d+", x), files)

    grouped = dict()

    for l in files:
        m = re.match("\s+(\d+-\d+-\d+).*(-?\d+\.\d+)", l)
        grouped.setdefault(m.group(1), []).append(float(m.group(2)))

    for k,v in grouped.items():
        result.setdefault(k, {})["dst"] = sum(v)/len(v)


def load_solar_data():
    path_to_files = "../data/solar"

    if not exists(path_to_files):
        call(["wget", LINK, '-O', 'solar.tar.gz'])
        call(["tar", "zxvf", 'solar.tar.gz'])
        call(["mv", "744860", path_to_files])
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

    parse_dst(result)

    for k, v in grouped_by.items():
        result[k] = dict()

        for name in chosen_columns.keys():
            result[k][name] = int(sum(map(lambda i: float(i[name]), v)) / len(v))

    return result

if __name__ == '__main__':
    qq = load_solar_data()
    print(len(qq))
