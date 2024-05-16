import json
from os import path

CONSTANTS_DIR = path.dirname(__file__)


def get_keywords_dict() -> dict[str, list[str]]:
    # Rules for the keywords.json file:
    # - The file should be a JSON file
    # - Each key in the JSON file should be a string that is in properly formatted
    #   title case intended for display to the user
    #   i.e. "Commodities" instead of "commodities",
    #        "Ethylene Glycol" instead of "ethyleneglycol"
    # Try not to add weird characters in the key, like emojis or special characters

    # The schema for the JSON file probably needs to change, using a JSON key as a
    # display string is bad jeebies and may result in a lot of problems in the future.

    with open(path.join(CONSTANTS_DIR, "keywords.json")) as f:
        return json.load(f)
