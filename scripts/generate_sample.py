import csv

sample_rows = 2000
outdata = []
with open('../data/winred/sa_winred_july_2021_midyear.csv', 'r') as f:
    infile = csv.DictReader(f)
    for _ in range(sample_rows):
        outdata.append(next(infile))

with open('../data/winred/samples/sa_winred_2021_sample.csv', 'w') as f:
    outfile = csv.DictWriter(f, fieldnames=list(outdata[0].keys()))
    outfile.writeheader()
    for row in outdata:
        outfile.writerow(row)
