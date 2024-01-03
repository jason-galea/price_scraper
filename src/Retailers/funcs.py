from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions


### TODO: Start FF globally, reuse class to avoid MEM spikes
def create_webdriver() -> webdriver.Firefox:
    """
    Launches new webdriver
    """

    ff_opts = FirefoxOptions()
    ff_opts.add_argument('-headless')
    # ff_cap = DesiredCapabilities.FIREFOX
    # ff_cap["marionette"] = True
    # ff_opts.set_capability("marionette", True)

    return webdriver.Firefox(
        service=Service(executable_path="/usr/local/bin/geckodriver"),
        options=ff_opts,
        # capabilities=ff_cap,
    )


def concat_items_in_list(input_list: list, start_index: int, end_index: int) -> list:
    """
    Receives list & two indexes.\n
    Returns list with elements between the indexes concaternated (inclusive).\n
    E.G: concat_items_in_list(["a", "b", "c", "d"], 1, 2) --> ["a", "b c", "d"]
    """
    result_list = input_list
    for _ in range(end_index - start_index):
        result_list[start_index] = f"{input_list[start_index]} {input_list[start_index + 1]}"
        del result_list[start_index + 1]

    return result_list


# def remove_strings_from_list(l: list, strings_to_remove: list) -> list:
#     """
#     """
#     return [ s for s in l if (s not in strings_to_remove) ]
