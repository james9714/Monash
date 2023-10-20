with open('ass2 - copy/Assignment 2 Template  Data/data/stock.txt') as f:
    data = f.readlines()
data = [x.strip().split(', ') for x in data]
for line in data:
    print(line[0])
    print(','.join(line[6:]))