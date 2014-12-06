import csv
import datetime
import re

year_re = re.compile("[0-9]{4}")
phases = ['N', 'F', 'S', 'L']
phase_dates = []
with open("raw_moon.txt",'r') as raw_data:
    current_year = None
    begin_of_year = False


    for line in raw_data.readlines():
        line = line.strip()
        if not line:
            continue
        words = line.split('   ')
        if words[0]:
            if words[0][0] in ['Y','P','U']:
                continue
            if year_re.match(words[0]):
                current_year = words[0]
                words[0] = ' '
                begin_of_year = True

        dates = []
        for word in words:
            word = word.strip()
            if len(word) < 13:
                continue
            if len(word) > 13:
                word = word[0:13]
            dates.append(datetime.datetime.strptime(current_year+' '+word, "%Y %b %d  %H:%M"))
        if begin_of_year:
            dif = len(phases) - len(dates)
            begin_of_year = False
        else:
            dif = 0

        for i,d in enumerate(dates):
            phase_dates.append([d, phases[i+dif]])
print(phase_dates)

with open("moon.csv",'w') as csv_data:
    writer = csv.writer(csv_data)
    day_number = None
    for i,(d, p) in enumerate(phase_dates):
        writer.writerow((d.strftime("%Y %b %d  %H:%M"), p))
        # if p == 'N':
        #     day_number = 1
        # if i == 0 or day_number is None:
        #     continue
        #
        # prev_date, prev_phase = phase_dates[i-1]
        # while prev_date < d:
        #     writer.writerow([prev_date.strftime("%Y-%m-%d"), str(day_number)+"d"])
        #     prev_date += datetime.timedelta(days=1)
        #     day_number += 1