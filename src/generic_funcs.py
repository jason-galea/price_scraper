
# def get_json_filenames() -> list:
#     return glob(f"{JSON_OUTPUT_DIR}/*.json")

def list_contains_all_values(haystack, needles) -> bool:
    return all((n in haystack) for n in needles)
