#!/usr/local/opt/python@3.8/bin/python3
import csv

# START HERE: update segments for 4
#
# Other future ones:
# 2.1 2.2 2.6 2.8 2.9 2.10 2.14
# 4 5 7 10 11 13 14 15 16 17 21
# umm...just check every one, and after hack the script to compare
#
# 2 4 and 5:
# https://discourse.suttacentral.net/t/continuation-of-discussion-for-bilara-users/16477/158?u=tracy
# https://github.com/suttacentral/bilara-data/commit/335f5cac1798b3af5c05952155d3cecc4dd8edd2
#
# 7:
# https://discourse.suttacentral.net/t/continuation-of-discussion-for-bilara-users/16477/188?u=tracy
#
# 10 11 13 16 17
# https://discourse.suttacentral.net/t/continuation-of-discussion-for-bilara-users/16477/210?u=tracy
# https://discourse.suttacentral.net/t/continuation-of-discussion-for-bilara-users/16477/217?u=tracy
# https://discourse.suttacentral.net/t/continuation-of-discussion-for-bilara-users/16477/228?u=tracy
#
# 14 15
# https://discourse.suttacentral.net/t/continuation-of-discussion-for-bilara-users/16477/213?u=tracy
#
# 21
# https://discourse.suttacentral.net/t/continuation-of-discussion-for-bilara-users/16477/245?u=tracy
#
# checks:
# x segments match
# x all references appear in order
# x starts and ends are spit out for good measure
#
# grab the reference file and insert them in the right order

# Files!
input_file = "ref1.2.csv"
assert input_file[:3] == "ref" and input_file[-4:] == ".csv", "Funky filename.  Expected filename ref[blah].csv"

chapter = input_file[3:-4]
root_filename = f"/Users/tracy/Development/bilara-data/root/pli/ms/vinaya/pli-tv-pvr/pli-tv-pvr{chapter}_root-pli-ms.json"

# Run through csv and collect data in various handy ways.
csv_segments = []
pts_vp_en = []
pts_cs = []
pm = []
references = {}
with open(input_file) as c:
    csv_reader = csv.reader(c, delimiter="\t")
    for row in csv_reader:
        csv_segments.append(row[0])
        if row[2]:
            pts_vp_en.append(row[2])
            references.setdefault(row[0], []).append(row[2])
        if len(row) >= 4 and row[3]:
            pts_cs.append(row[3])
            references.setdefault(row[0], []).append(row[3])
        if len(row) >= 5 and row[4]:
            pm.append(row[4])
            references.setdefault(row[0], []).append(row[4])

# Slurp up and pick out all segment numbers from root file.
root_segments = []
with open(file=root_filename) as f:
    for line in f.readlines():
        if line.strip() in ("{", "}"):
            continue
        root_segments.append(line.strip().rstrip(",").split(": ", 1)[0].strip('"'))

# Check that segment numbers match between root file and csv.
#for i in range(min(len(root_segments), len(csv_segments))):
#    print(f"{root_segments[i]:25}{csv_segments[i]}")
assert root_segments == csv_segments, "Segments do not agree."

# Check that all page numbers appear in order.
prev = False
ref_prefix = "pts-vp-en6."
for ref in pts_vp_en:
    assert ref.startswith(ref_prefix)
    page = int(ref[len(ref_prefix):])
    if prev:
        assert prev + 1 == page
    else:
        print(f"Starts at page {page}.")
    prev = page
print(f"Ends at page {prev}.")

# Check that all pts-cs references appear in order and display the ranges.
prev_bits = False
prev_ref = False
start = False
ref_prefix = "pts-cs"
for ref in pts_cs:
    assert ref.startswith(f"{ref_prefix}{chapter}.")  # e.g. "pts-cs2.1."
    if not start:
        start = ref
    bits = ref[len(ref_prefix):].split(".")
    bits = [int(x) for x in bits]
    num_bits = len(bits)
    if prev_bits:
        assert prev_bits < bits, f"prev: {prev_bits} current: {bits}"
        if bits[-1] != prev_bits[-1] + 1:
            # Last bit isn't consecutive.
            assert num_bits > 2
            if bits[-2] != prev_bits[-2] + 1:
                # Second last bit isn't consecutive.
                assert num_bits > 3
                assert bits[-3] == prev_bits[-3] + 1
            else:
                # This is only useful if we have 4 bits.
                assert bits[:-2] == prev_bits[:-2]
            print(f"{start} - {prev_ref}")
            start = ref
        else:
            # Last bit is consecutive.  Check all previous bits are equal.
            assert bits[:-1] == prev_bits[:-1]
    prev_bits = bits
    prev_ref = ref

# Check that pm references appear in order and display the ranges.
prev_class = False
prev_number = False
start = False
sangha = False
ref_prefix = "pm-"
for ref in pm:
    assert ref.startswith(ref_prefix)
    if sangha:
        assert sangha == ref[3:5]
    else:
        sangha = ref[3:5]  # "bi" or "bu"
    assert ref[5] == "-"
    rule_class = ref[6:8]  # "pj" or "sk" or ...
    rule_number = int(ref[8:])
    if not start:
        start = ref
    if prev_class:
        if rule_number != prev_number + 1:
            assert prev_class != rule_class, f"prev: {prev_class}{prev_number} curr: {rule_class}{rule_number}"
            print(f"{start} - {ref_prefix}{sangha}-{prev_class}{prev_number}")
            start = ref
        else:
            assert prev_class == rule_class
    prev_class = rule_class
    prev_number = rule_number