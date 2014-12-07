import csv
import datetime
import re


def prepare_phase():
    year_re = re.compile("[0-9]{4}")
    phases = ['N', 'F', 'S', 'L']
    phase_dates = []
    with open("../moon_data/raw_moon.txt",'r') as raw_data:
        current_year = None
        begin_of_year = False

        for line in raw_data.readlines():
            line = line.strip()
            if not line:
                continue
            words = line.split('   ')
            if words[0]:
                if words[0][0] in ['Y', 'P', 'U']:
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
                flag = '-'
                if len(word) > 13:
                    flag = word[13:]
                    word = word[0:13]
                dates.append((datetime.datetime.strptime(current_year+' '+word, "%Y %b %d  %H:%M"), flag))
            if begin_of_year:
                dif = len(phases) - len(dates)
                begin_of_year = False
            else:
                dif = 0

            for i,(d,f) in enumerate(dates):
                phase_dates.append([d, phases[i+dif], f])
    print(phase_dates)

    with open("../moon_data/moon_phase.csv",'w') as csv_data:
        writer = csv.writer(csv_data)
        for i,(d, p, f) in enumerate(phase_dates):
            writer.writerow((d.strftime("%Y %b %d  %H:%M"), p, f))

prepare_phase()