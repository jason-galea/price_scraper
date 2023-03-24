import os
# import datetime
# import enum
import json


### COMMON FUNCTIONS
def concaternate_items_within_list(input_list: list, start_index: int, end_index: int) -> list:
    """
    Receives list & two indexes.\n
    Returns list with elements between the indexes concaternated (inclusive).\n
    E.G: concaternate_items_within_list(["a", "b", "c", "d"], 1, 2) --> ["a", "b c", "d"]
    """
    result_list = input_list
    for _ in range(end_index - start_index):
        result_list[start_index] = f"{input_list[start_index]} {input_list[start_index + 1]}"
        del result_list[start_index + 1]

    return result_list

def remove_multiple_strings_from_list(l: list, strings_to_remove: list) -> list:
    return [s for s in l if (s not in strings_to_remove)]

def export_json(extracted_data: iter, dir: str, file: str) -> None:
    print(f"\nExporting data to {file}\n")

    ### Check/Create dir
    if not os.path.exists(dir):
        os.makedirs(dir)

    ### Write
    with open(file, "w") as f:
        f.write(json.dumps(extracted_data))
