import csv
import sys


def main():
    if len(sys.argv) < 3:
        print("ERROR: Must pass in infile and outfile as arguments.")
        print(
            "Expected command format: python generate_sample.py [infile_path] [outfile_path]")
        return

    infile_path = sys.argv[1]
    outfile_path = sys.argv[2]

    sample_rows = 2000
    outdata = []
    with open(infile_path, 'r') as f:
        infile = csv.DictReader(f)
        for _ in range(sample_rows):
            outdata.append(next(infile))

    with open(outfile_path, 'w') as f:
        outfile = csv.DictWriter(f, fieldnames=list(outdata[0].keys()))
        outfile.writeheader()
        for row in outdata:
            outfile.writerow(row)


if __name__ == "__main__":
    main()
