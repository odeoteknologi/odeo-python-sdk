from odeo.api_signature import generate_signature


def test_generate_signature():
    signing_key = "W7dN7zfbMWrLvOILW6Q1"

    expected = "TM/rrLRD1reOodDe7Ulk0kxGqw33Ufcmbse+eZPlSW0="
    actual = generate_signature(
        "POST",
        "/some/path",
        "",
        "4cc355T0k3n",
        1234567890,
        '{"test":12345}',
        signing_key,
    )

    assert actual == expected


def test_generate_signature_from_doc():
    signing_key = "Key"

    expected = "JhWklt2rgpFYreQ88U5StXNdkJFfmOlumstoR1J+x+k="
    actual = generate_signature(
        "GET",
        "/path",
        "",
        "token",
        123456,
        "",
        signing_key,
    )

    assert actual == expected


def test_generate_signature_for_webhook():
    signing_key = "D2skZLj6nqgDgtI48fi4vDsv2jhvSUDlMnb6HGTFWM3G8Vx4UE3dmN0N6oRc3FxM"

    expected = "AmpNklPeoB2w+G6k+bDGAiTdejGQW9weOa8CzAZxh7c="
    actual = generate_signature(
        "POST",
        "/webhook-va-inquiry",
        "",
        "",
        1641542946,
        '{"notify_type":"va_inquiry","va_code":"89910232564212"}',
        signing_key,
    )

    assert actual == expected
