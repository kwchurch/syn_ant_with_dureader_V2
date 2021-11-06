import sys,csv,json

def row2dict(fields, row):
    res = {}
    for f,r in zip(fields,row):
        res[f]=r
    return res

for csvf in sys.argv[1:]:
    with open(csvf, 'r') as fd:
        csvreader = csv.reader(fd)
        fields = next(csvreader)
        j = [ row2dict(fields, row) for row in csvreader ]
    jsonf = csvf[0:-3]+'json'
    with open(jsonf, 'w') as fd2:
        json.dump(j, fd2)
        
