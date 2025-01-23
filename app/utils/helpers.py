import random
import time


def generate_amazon_session_id():
    """Generates a random Amazon session ID."""
    return f"{random.randint(100, 999)}-{random.randint(1000000, 9999999)}-{int(time.time() * 1000) % 10000000}"


def get_safe_value(data, keys):
    """
    Safely retrieves a value from a nested dictionary.
    """
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError):
            return None
    return data


def parse_release_dates(title_data):
    """
    Parses release dates from the title data, including digital release dates.
    """
    release_dates = []
    edges = get_safe_value(title_data, ["releaseDates", "edges"])
    if edges:
        for edge in edges:
            node = get_safe_value(edge, ["node"])
            if node:
                release_date = {
                    "month": get_safe_value(node, ["month"]),
                    "day": get_safe_value(node, ["day"]),
                    "year": get_safe_value(node, ["year"]),
                    "country_id": get_safe_value(node, ["country", "id"]),
                    "release_type": None,  # Initialize release_type
                    "attributes": [],
                }

                attributes = get_safe_value(node, ["attributes"])
                if attributes:
                    for attribute in attributes:
                        attr_id = get_safe_value(attribute, ["id"])
                        release_date["attributes"].append(attr_id)
                        if attr_id == "internet":  # Check if its a digital release
                            release_date["release_type"] = "digital"

                    # if no internet found in attributes, then consider it as theatrical release
                    if release_date["release_type"] is None:
                        release_date["release_type"] = "theatrical"

                release_dates.append(release_date)
    return release_dates
