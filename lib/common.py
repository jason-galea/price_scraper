#!/usr/bin/python3

import os
import datetime
import enum
import json


### COMMON FUNCTIONS
def concaternate_items_within_list(l, i, j):
    ### Receives list & two indexes
    ### Returns list with elements between the indexes concaternated (inclusive)
    ### E.G: concaternate_items_within_list(["a", "b", "c", "d"], 1, 2) --> ["a", "b c", "d"]
    for _ in range(j - i):
        l[i] = f"{l[i]} {l[i + 1]}"
        del l[i + 1]

    return l

def remove_multiple_strings_from_list(l=list, strings_to_remove=list):
    return [s for s in l if (s not in strings_to_remove)]
