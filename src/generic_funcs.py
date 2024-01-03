import datetime

# def get_json_filenames() -> list:
#     return glob(f"{JSON_OUTPUT_DIR}/*.json")

def list_contains_all_values(haystack, needles) -> bool:
    return all((n in haystack) for n in needles)


def get_utcnow_iso_8601() -> str:
    """
    Get current UTC time in ISO 8601 standard format
    """
    return get_iso_8601_time(datetime.datetime.utcnow())

def get_iso_8601_time(dt: datetime.datetime):
    """
    Convert any datetime object to ISO 8601 standard format
    """
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

