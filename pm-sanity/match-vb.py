#!/usr/bin/env python3

import os
import subprocess

## Set up directories and filenames.
CWD = os.getcwd()
VINAYA_PATH = "/Users/tracy/Development/bilara-data/translation/en/brahmali/vinaya"

bi_pm_file = f"{VINAYA_PATH}/pli-tv-bi-pm_translation-en-brahmali.json"
bu_pm_file = f"{VINAYA_PATH}/pli-tv-bu-pm_translation-en-brahmali.json"

bi_pm_vb_segments_file = "pm-to-vb-bi.csv"
bu_pm_vb_segments_file = "pm-to-vb-bu.csv"

def isSegmentRange(text):
    """
    Given a string, returns True if the string contains a segment range.
    Assumes this is formatted in "{from segment} - {to segment}"
    """
    return " - " in text

def isSegmentId(text):
    """
    Given a string, returns True if the string is a valid SC segment ID.
    """
    return True

def make_segment_id_dict(csv_file):
    """
    Create a dictionary of pm segment IDs to vb segment IDs.
    """
    lookup = {}
    f = open(file=csv_file)
    return lookup

def get_segment_text(segment_id):
    """
    Return the translation text given a segment ID.
    """
    os.chdir(VINAYA_PATH)
    output = subprocess.run(["ag", f'{segment_id}:', "--nofilename"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    os.chdir(CWD)
    # TODO decide whether to leave segment id bit in or not
    # yeah...we need to get just the text, START HERE
    return output

def check_same_text(pm_file):
    """
    For a pm file, check all its text matches with equivalent vb segments.
    """
    seen_first_line = False
    seen_last_line = False

    f = open(file=pm_file)
    all_lines = f.readlines()
    for line in all_lines:
        if line == '{\n':
            seen_first_line = True
        elif line.strip() == '}':
            seen_last_line = True
        elif seen_first_line and not seen_last_line:
            check_line(line)

def check_line(line):
    """
    For a content line in a pm file, check whether there is an equivalent segment
    in the vb and complain if the text doesn't agree.  Or something like that.
    """
    (segment_id, segment_text) = line.strip().rstrip(",").split(": ", 1)
    print(f"{segment_id}...{segment_text}")




def compare(key_file):
    """
    For each line in the key csv file, check that the segments have the same text,
    or if it is not a vb segment ID, check that the heading is in order.
    """
    with open(key_file) as csv_file:
        for line in csv_file:
            [pm_sid, vb_sid] = line.strip().split(",")
            # Get the text for the pm entry.
            # Sometimes the entry in the csv file is a range of segments rather
            # than a single segment ID.  If it is a range, grab the segment texts
            # and concatenate.
            pm_stext = ""
            if " - " in pm_sid:
                [pm_sid_from, pm_sid_to] = pm_sid.split(" - ")
                # Since the CSV data currently only has pm segment ranges of 2,
                # we're just going to assume there are no segments in between
                # the from and to segments.  We're not even going to write an
                # assert (yet).
                pm_stext = get_segment_text(pm_sid_from) + " " + get_segment_text(pm_sid_to)
            else:
                pm_stext = get_segment_text(pm_sid)

            # Check whether the second entry is a segment ID.  If it isn't we're
            # checking whether the rule title has the right number.

            # Get the text for the segments.
            # Sometimes the entry in the csv file is a range of segments rather
            # than a single segment ID.  If it is a range, grab the segment texts
            # and concatenate.

            print(f"{pm_sid} ... {pm_stext}")

# Run!
compare(bu_pm_vb_segments_file)
#check_same_text(bu_pm_file)
