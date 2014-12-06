import csv
import datetime

rises = []
with open("new_york_raw_moon.txt" ,'r') as inp:
    cur_year = None

    for line in inp.readlines():
        line = line.strip()
        if not line:
            continue
        if "the Moon for" in line:
            cur_year = int(line[79:85])
        if line[0] in '0123456789':
            line = line.replace('     ', ' -')
            words = line.split()
            day = int(words[0])
            rise = True
            month = 1
            for w in words[1:]:
                w = w.strip()
                if not w:
                    continue
                if rise and w != '-':

                    h = int(w[0:2])
                    m = int(w[2:4])
                    rises.append(datetime.datetime(cur_year, month, day, h, m))
                if not rise:
                    month += 1

                rise = not rise

new_moons = []
with open("moon.csv") as moon_file:
    reader = csv.reader(moon_file)
    for k in  reader:
        if k[1] == 'N':
            new_moons.append(datetime.datetime.strptime(k[0],"%Y %b %d  %H:%M"))

rises += new_moons

rises = sorted(rises)
with open("ny_moon_dates.csv", 'w') as csv_out:
    writer = csv.writer(csv_out)
    day = None
    for r in rises:
        if r in new_moons:
            day = 1
        if day is not None:
            writer.writerow((r.strftime("%Y %b %d  %H:%M"), str(day)+'d'))
            day += 1