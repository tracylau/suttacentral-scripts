#!/usr/bin/env python3

## Set up filenames.
bilara_data_path = "../../bilara-data"

bi_pm_file = f"{bilara_data_path}/translation/en/brahmali/vinaya/pli-tv-bi-pm_translation-en-brahmali.json"
bu_pm_file = f"{bilara_data_path}/translation/en/brahmali/vinaya/pli-tv-bu-pm_translation-en-brahmali.json"

bi_pm_vb_segments_file = "pm-to-vb-bi.csv"
bu_pm_vb_segments_file = "pm-to-vb-bu.csv"

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
    Return the translation text given a segment ID.  For vb segment IDs only.

    Raises ValueError if segment ID is invalid.
    Raises RuntimeError if segment cannot be found.
    """
    return "foobar"

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
    (segment_id, segment_text) = line.strip().rstrip(",").split(": ", 1)
    print(f"{segment_id}...{segment_text}")

# Run!
check_same_text(bi_pm_file)
check_same_text(bu_pm_file)
