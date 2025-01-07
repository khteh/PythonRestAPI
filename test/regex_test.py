import pytest, logging, os, re
from re import Match
"""
$ pytest regex_test.py
"""
NUMBER_REGEX_TEST_CASES = [
    ("123", True),
    ("Hello World", False),
    ("123 ", False),
    (" 123", False),
    ("123.", False),
    ("123-", False),
    ("-123", False),
]
@pytest.mark.parametrize("data, expected", NUMBER_REGEX_TEST_CASES)
def test_numberRegex(data, expected):
    numberRegex = r"^(\d)+$"
    assert expected == bool(re.match(numberRegex, data))

STRING_REGEX_TEST_CASES = [
    ("Hello World", True),
    ("Hello-World", True),
    ("Hello_World", True),
    ("Hello World 123", True),
    ("Hello World!!!", False),
    ("Hello World ~!@#$%^&*()_+", False),
]
@pytest.mark.parametrize("data, expected", STRING_REGEX_TEST_CASES)
def test_stringRegex(data, expected):
    regex = r"^([\w\d\-_\s])+$"
    assert expected == bool(re.match(regex, data))

STRING_LENGTH_REGEX_TEST_CASES = [
    ("Hello-Worl", True),
    ("Hello-Worl", True),
    ("HelloWorl8", True),
    ("Helo", False),
    ("HelloWorl89", False),
    ("Hello World ~!@#$%^&*()_+", False),
]
@pytest.mark.parametrize("data, expected", STRING_LENGTH_REGEX_TEST_CASES)
def test_stringLengthRegex(data, expected):
    regex = r"^([\w\d\-_\s]){5,10}$"
    assert expected == bool(re.match(regex, data))

LETTERS_REGEX_TEST_CASES = [
    ("HelloWorld", True),
    ("HelloWorl0", False),# Should NOT match due to number
    ("Hello Worl", False),# Should NOT match due to space
    ("Hello World", False), # Should NOT match due to length
]
@pytest.mark.parametrize("data, expected", LETTERS_REGEX_TEST_CASES)
def test_lettersRegex(data, expected):
    lettersRegex = r"^([a-zA-Z]){0,10}$"
    assert expected == bool(re.match(lettersRegex, data))

EMAIL_REGEX_TEST_CASES = [
    ("", False),
    (".@.", False),
    ("-@-", False),
    ("a@", False),
    ("ab@de", False),
    ("abc@def", False),
    ("a@b.c", False),
    ("~!@#$%^&*()_+@b.c", False),
    ("~!#$%^&*()_+@b.c", False),
    ("kokhow.teh@b.c", False),
    ("kokhow teh@b.c", False),
    ("kok-how_teh@b.c", False),
    ("kok-how_teh@b.c.d", False),
    ("123@456", False),
    ("123@ntu.edu.sg", True),
    ("me@gmail.com", True),
    ("tan_k_h@gmail.com", True),
    ("tan-k.h@gmail.com", True),
    ("tan-k.h@gmail.co.uk", True),
    ("tan k h@gmail.com", False)
]
@pytest.mark.parametrize("data, expected", EMAIL_REGEX_TEST_CASES)
def test_emailRegex(data, expected):
    emailRegex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    assert expected == bool(re.match(emailRegex, data))

NUMERIC_LENGTH_REGEX_TEST_CASES = [
    ("1234567", False),
    ("12345678", True),
    ("123456789", True),
    ("1234567890", True),
    ("12345678901", False)
]
@pytest.mark.parametrize("data, expected", NUMERIC_LENGTH_REGEX_TEST_CASES)
def test_numericRegex(data, expected):
    regex = r"^(\d{8,10})$"
    assert expected == bool(re.match(regex, data))

PHONE_NUMBER_REGEX_TEST_CASES = [
    ("1234567", False),# Invalid due to length < 8
    ("12345678", True),
    ("1234567890", True),
    ("12345678901", False),# Invalid due to length > 10
    ("+6512345678", True),
    ("+65-12345678", True),
    ("+ab-91234567", False),
    ("+65 91234567", False),# Invalid due to space
    ("+123-1234567", False),# Invalid due to length < 8
    ("+123-12345678", True),
    ("+123-1234567890", True),
    ("+123-12345678901", False),# Invalid due to length > 10
    ("+-1234567890", False),# Invalid due to country code < 1
    ("-1234567890", False),# Invalid due to country code < 1
    ("+1234-1234567890", False),# Invalid due to country code > 3
    ("+123-HelloWorld", False),
    ("+123-", False)
]
@pytest.mark.parametrize("data, expected", PHONE_NUMBER_REGEX_TEST_CASES)
def test_phoneNumberRegex(data, expected):
    # 91234567, +123-1234567890
    phoneRegex = r"^(\+\d{1,3}\-?)*(\d{8,10})$"
    assert expected == bool(re.match(phoneRegex, data))

def test_SringContainsAlphabets():
    assert re.search('[a-zA-Z]',"Hello World!!! 123")
    assert not re.search('[a-zA-Z]',"123")