#!/usr/bin/env python3

from collections import OrderedDict
import json
import os


def new_filename(filename, data_type):
    assert filename[-5:] == ".json", f"{filename} is not a .json file"
    assert data_type in ("name", "tree")
    return filename[:-5] + "-" + data_type + ".json"

def name_filename(filename, debug=False):
    if debug:
        return "./name-sandbox.json"
    return new_filename(filename, "name")

def tree_filename(filename, debug=False):
    if debug:
        return "./tree-sandbox.json"
    return new_filename(filename, "tree")

def split_file(filename, debug=False):
    # Read in .json file.
    with open(filename) as f:
        data = json.load(f)

    # These will hold the final structures we need.
    tree = OrderedDict()
    names = OrderedDict()

    # Cheat.  Go over all the nodes and record whether it is the parent of a leaf node.
    previous_entry = None
    for entry in data:
        if "type" in entry and entry["type"] != "text":
            entry["grandparent"] = True
        else:
            if previous_entry["grandparent"]:
                previous_entry["grandparent"] = False
            entry["grandparent"] = False
        previous_entry = entry

    # Each .json file turns into a list of dicts.
    # Go through each element and pick out the _path and name elements and do
    # whatever we need to do with them.
    for entry in data:
        # Assert that there are no keys that have not been mentioned in the ticket.
        for key in entry.keys():
            assert key in ["_path", "name", "num", "child_count", "display_num", "type", "acronym", "volpage", "biblio_uid", "grandparent"], f"Unknown key found: {key}"

        # To create the tree, we need to split up the path into bits, and then make
        # a tree.
        split_path = entry["_path"].split("/")
        # Just to get past gdhp.json, pdhp.json
#        if split_path[0] == '':
#            split_path = split_path[1:]
        # END HACK
        # Traverse the tree until we are at the point where we insert this entry.
        parent = tree
        for i in range(len(split_path) - 1):
            # START HACK for minor-lzh, other-san, other-xct
#            if split_path[i] not in parent:
#                parent[split_path[i]] = {}
            # END HACK
            parent = parent[split_path[i]]

        print(split_path)  # TODO remove - debugging
        if "type" in entry and entry["type"] != "text":
            # This is a division or subdivision.  Add it as a key with value [] if
            # the next level will be suttas, {} otherwise.
            if not entry["grandparent"]:
                parent[split_path[-1]] = []
            else:
                parent[split_path[-1]] = OrderedDict()
        else:
            # This is a sutta/text i.e. a leaf.  Append it to the array.
            parent.append(split_path[-1])

        # To create the name lookup, we just need the last bit of the path.
        assert split_path[-1] not in names, f"UID {split_path[-1]} appears more than once."
        names[split_path[-1]] = entry["name"]

    if debug:
        import pprint
        pprint.pprint(names)
        pprint.pprint(tree)

    with open(name_filename(filename, debug), 'w') as json_file:
        json.dump(names, json_file, indent = 2, ensure_ascii=False)
    with open(tree_filename(filename, debug), 'w') as json_file:
        json.dump(tree, json_file, indent = 2, ensure_ascii=False)

# Loop over all .json files.
directory = "/Users/tracy/Development/sc-data/structure/division"
ignore = [
    "/Users/tracy/Development/sc-data/structure/division/sutta/dharmapadas.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/kn.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/dharmapadas/gdhp.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/dharmapadas/lzh-dhp.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/dharmapadas/pdhp.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/dharmapadas/uv.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/dharmapadas/uvs.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/dharmapadas/xct-uv.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/minor-lzh/lzh-dharani.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/minor-lzh/lzh-ja.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/minor-lzh/lzh-nbs.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/minor-lzh/lzh-ssnp.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/minor-lzh/lzh-svk.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/other/other-san/arv.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/other/other-san/avs.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/other/other-san/divy.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/other/other-san/lal.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/other/other-san/mkv.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/other/other-san/sf.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/other/other-san/sht.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/other/other-san/ybs.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/other/other-xct/d.json",
    "/Users/tracy/Development/sc-data/structure/division/sutta/other/other-xct/up.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-dg-bi-pm.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-dg-bu-pm-2.json",
    "/Users/tracy/Development/sc-data/structure/division/vinaya/lzh-dg-bu-pm.json",
]
for root, dirs, files in os.walk(directory):
    for file in files:
        filename = os.path.join(root, file)
        if filename in ignore:
            print(f"SKIPPING {filename}")
            continue
        print(f"Processing {filename}")
        #split_file(filename, debug=True)
