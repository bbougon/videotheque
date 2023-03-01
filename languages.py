_LANGUAGES = {
    "PORTUGUESE": "PORTUGUESE",
    "PT": "PORTUGUESE",
    "BR": "PORTUGUESE",
    "FRENCH": "FRENCH",
    "FR": "FRENCH",
    "FRE": "FRENCH",
    "ENG": "ENGLISH",
    "EN": "ENGLISH",
    "US": "ENGLISH",
    "VOSTFR": "VOSTFR",
}


def extract_languages_from_name(file_name):
    flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]
    flatten_file_name = flat_map(
        lambda x: x, [el.split(" ") for el in file_name.split(".")]
    )
    return [
        language
        for key, language in _LANGUAGES.items()
        if key in flatten_file_name or key.casefold() in flatten_file_name
    ]
