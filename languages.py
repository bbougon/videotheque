from typing import List

_LANGUAGES = {
    "BR": "PORTUGUESE",
    "EN": "ENGLISH",
    "ENG": "ENGLISH",
    "FR": "FRENCH",
    "FRA": "FRENCH",
    "FRE": "FRENCH",
    "FRENCH": "FRENCH",
    "Ita": "ITALIAN",
    "It": "ITALIAN",
    "PORTUGUESE": "PORTUGUESE",
    "POR": "PORTUGUESE",
    "PT": "PORTUGUESE",
    "Spa": "SPANISH",
    "US": "ENGLISH",
    "VOSTFR": "VOSTFR",
}


def extract_languages_from_name(file_name) -> List[str]:
    flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]
    flatten_file_name = flat_map(
        lambda x: x, [el.casefold().split(" ") for el in file_name.split(".")]
    )
    return map_languages(flatten_file_name)


def map_languages(languages: List[str]):
    return [
        language
        for key, language in _LANGUAGES.items()
        if key.casefold() in languages
    ]
