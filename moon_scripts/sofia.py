import csv
import operator

def process_sofia(input, output):
    result = dict()
    with open(input, 'rb') as file:
        reader = list(csv.reader(file, delimiter = ','))[1:]
        for row in reader:
            prev = [0] * 10
            if row[0] in result:
                prev = result[row[0]]
            if (row[0] != row[1]):
                pass
            else:
                try:
                    result[row[0]] = map(operator.add, prev, map(int, row[2:]))
                except ValueError:
                    pass
    with open(output, 'wb') as file:
        writer = csv.writer(file)
        for key in sorted(result):
            writer.writerow([key] + result[key])

if __name__ == '__main__':
    process_sofia("../data/sofiaDTP.csv", "../data/sofia.csv")
