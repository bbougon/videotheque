from languages import extract_languages_from_name


def test_should_return_languages():
    languages = extract_languages_from_name(
        " 01 Shrek - Animation 2001 Eng Fre Ita Spa Multi-Subs 1080p [H264-mp4]"
    )

    assert languages == ["ENGLISH", "FRENCH", "ITALIAN", "SPANISH"]
