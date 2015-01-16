import csv
from subprocess import call

def load_aviation_as_dict():
    call(['Rscript', 'aviation.R'])
    output = '../data/AviationDates.csv'
    data = csv.reader(open(output))
    result = {}
    for d, c in data:
        result[d] = c
    call(['rm', output])
    return result
