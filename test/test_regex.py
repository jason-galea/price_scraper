#!/usr/bin/env python3


import re
import json



def main():


    regex_result = re.search(
        pattern=r"(^[a-zA-Z\.]+) ([a-zA-Z\-\ 5]*)(\d+)GB \(((\d)x(\d+)GB)\) (\d{4}[MHhz]{3}) (CL\d{2}) +(DDR\d)(.*)",
        # string='Corsair Vengeance 32GB (2x16GB) 6000MHz CL40 DDR5', ### PASS
        string='Corsair Vengeance 48GB (2x24GB) 7000MHz C40 DDR5', ### FAIL
        # string='Team T-Force Delta RGB 64GB (2x32GB) 5200MHz CL40 Black', ### FAIL
    )

    print(regex_result.groups())

    # regex_groups_keys = ["Brand", "Model", "CapacityGB", "KitConfiguration", "SticksPerKit", "CapacityPerStick", "Clock", "CASPrimary", "MemoryType", "Misc"]
    # regex_groups_vals = [ val.strip() for val in regex_result.groups() ] ### Strip spaces
    # regex_groups_vals = [ (int(s) if (s.isdigit()) else s) for s in regex_groups_vals ] ### Convert ints to ints

    # # print(f"==> INFO: regex_groups_keys = {regex_groups_keys}")
    # # print(f"==> INFO: regex_groups_vals = {regex_groups_vals}")

    # regex_groups_dict = dict(zip( regex_groups_keys, regex_groups_vals ))



    # print(json.dumps(regex_groups_dict, indent=4))




if __name__ == '__main__':
    main()
