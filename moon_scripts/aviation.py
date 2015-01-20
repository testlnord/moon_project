import csv
from subprocess import call
import datetime

DATE_FORMAT = "%Y-%m-%d"

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def load_aviation_as_dict():
    call(['Rscript', 'aviation.R'])
    output = '../data/AviationDates.csv'
    data = csv.reader(open(output))
    result = {}
    for d, c in data:
        result[d] = c

    # 0 accidents
    start_date = datetime.datetime.strptime(min(result.keys()), DATE_FORMAT)
    end_date   = datetime.datetime.strptime(max(result.keys()), DATE_FORMAT)
    for n in daterange(start_date, end_date):
        s = n.strftime(DATE_FORMAT)
        if s not in result:
            result[s] = 0

    call(['rm', output])
    return result
