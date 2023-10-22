from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def instantiate_ff_driver_and_download(url: str):
    ### Options
    ff_opts = FirefoxOptions()
    ff_opts.add_argument('-headless')
    # ff_cap = DesiredCapabilities.FIREFOX
    # ff_cap["marionette"] = True
    # ff_opts.set_capability("marionette", True)

    driver = webdriver.Firefox(
        service=Service(executable_path="/usr/local/bin/geckodriver"),
        options=ff_opts,
        # capabilities=ff_cap,
    )

    ### Request page
    driver.get(url)

    return driver


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
    return [ s for s in l if (s not in strings_to_remove) ]


# def export_json(extracted_data: iter, dir: str, file: str) -> None:
#     print(f"==> INFO: Exporting data to '{file}'")

#     ### Check/Create dir
#     if not os.path.exists(dir):
#         os.makedirs(dir)

#     ### Write
#     with open(file, "w") as f:
#         f.write(json.dumps(extracted_data))


def export_to_db(extracted_data: list) -> None:
    print(f"==> INFO: Exporting data to db")
