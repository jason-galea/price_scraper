
# def get_json_filenames() -> list:
#     return glob(f"{JSON_OUTPUT_DIR}/*.json")

def listContainsAllValues(haystack, needles) -> bool:
    return all((n in haystack) for n in needles)
