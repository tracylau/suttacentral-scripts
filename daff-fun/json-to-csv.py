#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Convert a json bilara-data file into csv")
parser.add_argument("filename", help="The json file to convert")
parser.add_argument("--dest", action="store", dest="dest", help="Specify destination filename")
parser.add_argument("-v", action="store_true", help="Print each line of new file")
args = parser.parse_args()

json_filename = args.filename
if json_filename[-5:] != ".json":
    raise ValueError("Invalid file")

csv_filename = args.dest if args.dest else json_filename[:-4] + "csv"
print(f"creating {csv_filename}...")

with open(csv_filename, "w") as c:
    with open(json_filename) as f:
        for line in f:
            if line.strip() not in ["{", "}"]:
                [x, y] = line.strip().rstrip(",").split(": ", 1)
                if args.v:
                    print(x + "," + y + "\n")
                c.write(x + "," + y + "\n")
