import csv
import operator

def process_sofia(input, output):
    result = dict()
    with open(input, 'rb') as file:
        reader = list(csv.reader(file, delimiter=','))[1:]
        for row in reader:
            prev = [0] * 10
            if row[0] in result:
                prev = result[row[0]]
            if row[0] != row[1]:
                pass
            else:
                try:
                    result[row[0]] = map(operator.add, prev, map(int, row[2:]))
                except ValueError:
                    pass
    with open(output, 'wb') as file:
        writer = csv.writer(file)
        for key in sorted(result, reverse=True):
            writer.writerow([key] + [result[key][0]+result[key][1]])


def load_data_as_dict(inp_path="../data/sofiaDTP.csv"):
    result = dict()
    with open(inp_path, 'rb') as file:
        reader = list(csv.reader(file, delimiter=','))[1:]
        for row in reader:
            prev = [0] * 10
            if row[0] in result:
                prev = result[row[0]]
            if row[0] != row[1]:
                pass
            else:
                try:
                    result[row[0]] = map(operator.add, prev, map(int, row[2:]))
                    result[row[0]] = result[row[0]][0] + result[row[0]][1]
                except ValueError:
                    pass
    return result

if __name__ == '__main__':
    #process_sofia("../data/sofiaDTP.csv", "../data/sofia.csv")
    print(load_data_as_dict())
