import pytest, logging, os, re
from re import Match
"""
$ pipenv run pytest -v regex_test.py
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

CPP_CSHARP_REGEX_TEST_CASES = [
    ("C++", True),
    ("C#", True),
    ("C+", False),
    ("C##", False),
    ("C", True),
]
@pytest.mark.parametrize("data, expected", CPP_CSHARP_REGEX_TEST_CASES)
def test_cpp_csharpRegex(data, expected):
    # https://stackoverflow.com/questions/79435236/how-to-match-c-c-or-c
    # The ?: inside the group (?:\+\+|#) just make the group non capturing. The (?<!S) and (?!\S) are called lookarounds, and assert that either whitespace or the start/end precedes/follows the match
    # matches to be the entire input string
    cpp_csharp_regex = r"^C(?:\+\+|#)?$"
    # matches perhaps as part of a larger string, with the matches surrounded by whitespace
    #cpp_csharp_regex = r"\bC(?:\+\+|#)?(?!\S)"
    assert expected == bool(re.match(cpp_csharp_regex, data)) #If you want to catch these matches perhaps as part of a larger string, with the matches surrounded by whitespace

def test_SringContainsAlphabets():
    assert re.search('[a-zA-Z]',"Hello World!!! 123")
    assert not re.search('[a-zA-Z]',"123")

def test_log_format():
    text = "2025-04-04 05:44:55"
    regex = r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})?$"
    assert re.match(regex, text)

    text = " INFO "
    regex = r"^(\s)+INFO(\s)+?$"
    assert re.match(regex, text)

    text = " Running app..."
    regex = r"^(\s)+([\w\d\-_\.\s])+?$"
    assert re.match(regex, text)

    text = " INFO Running app..."
    regex = r"^(\s)+INFO(\s)+([\w\d\-_\.\s])+?$"
    assert re.match(regex, text)

    text = "2025-04-04 05:44:55 INFO Running app..."
    regex = r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})(\s)+INFO(\s)+([\w\d\-_\.\s])+?$"
    result = re.search(regex, text).groups()
    print(f"test_log_format result: {result}")

TIME_STRING_REGEX_TEST_CASES = [
    ("is 1 hour.", True),
    ("is 2 hours.", True),
    ("is 1 minute.", True),
    ("is 45 minutes.", True),
    ("is 1 hour and 1 minute.", True),
    ("is 1 hours and 45 minutes.", True),
    ("is 2 hours and 1 minute.", True),
    ("is 10 hours and 45 minute.", True)
]
@pytest.mark.parametrize("data, expected", TIME_STRING_REGEX_TEST_CASES)
def test_time_string(data, expected):
    regex = r"\b(\d+)(\s)+(hours?|minutes?)+"
    result = re.search(regex, data).groups()
    #print(f"test_time_string result: {result}")
    assert result
    assert result[0]

URI_REGEX_TEST_CASES = [
    ("www.google.com", False),
    ("http://www.google.com", True),
    ("https://www.google.com", True),
    ("127.0.0.1:8080", False),
    ("http://127.0.0.1:8080", True),
    ("https://127.0.0.1:4433", True),
    ("localhost:8080", False),
    ("http://localhost:8080", True),
    ("https://localhost:4433", True),
    ("[::1]:8080", False),
    ("http://[::1]:8080", True),
    ("https://[::1]:4433", True),
]
@pytest.mark.parametrize("data, expected", URI_REGEX_TEST_CASES)
def test_uri(data, expected):
    # The ?: inside the group (?:\+\+|#) just make the group non capturing.
    uri_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    assert expected == bool(re.match(uri_regex, data))

#def test_access_log_format():
#   text = "[2025-04-04 09:10:08 +0000] [10] [INFO] 192.168.0.149:34494 - - [04/Apr/2025:09:10:08 +0000] 'GET /health/live 2' 200 2 '-' 'kube-probe/1.27'"
#   regex = r"^[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\s)+[+-]{1}\d{4}](\s)+INFO(\s)+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5})(\s)+-\w-(\s)+[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}(\s)+(\s)+[+-]{1}\d4)](\s)+\"\w{[3,4}(\s)+(\w)+(\s)+\d\"(\s)+\d{3}(\s)+\d?$"

MONEY_REGEX_TEST_CASES = [
    ("$", False),
    ("$0.50", True),
    ("$123.50", True),
    ("$123", True),
    ("$123,456", True),
    ("$123,456,789", True),
    ("$123,456,789.50", True),
    ("$123.", True),
    ("$123,456,789.", True),
]
@pytest.mark.parametrize("data, expected", MONEY_REGEX_TEST_CASES)
def test_money(data, expected):
    money_regex = re.compile('|'.join([
        r'^\$?(\d*\.\d{1,2})$',  # e.g., $.50, .50, $1.50, $.5, .5
        r'^\$?(\d+)$',           # e.g., $500, $5, 500, 5
        r'^\$?(\d+\.?)$',         # e.g., $5.
        r'^\$?(\d+)(,\d{3})*$',           # e.g., $123,456, $1,234, $12,345
        r'^\$?(\d+)(,\d{3})*\.?$',         # e.g., $123,456.5, $1,234, $12,345
        r'^\$?(\d+)(,\d{3})*.\d{1,2}$',         # e.g., $123,456.5, $1,234, $12,345
    ]))
    assert expected == bool(re.match(money_regex, data))

STRING_MONEY_REGEX_TEST_CASES = [
    ("billed amount of $", False),
    ("billed amount of $0.50", True),
    ("billed amount of $123.50", True),
    ("billed amount of $123", True),
    ("billed amount of $123,456", True),
    ("billed amount of $123,456,789", True),
    ("billed amount of $123,456,789.50", True),
    ("billed amount of $123.", True),
    ("billed amount of $123,456,789.", True),
]
@pytest.mark.parametrize("data, expected", STRING_MONEY_REGEX_TEST_CASES)
def test_string_contains_money(data, expected):
    money_regex = re.compile('|'.join([
        r'\b\$?(\d*\.\d{1,2})',  # e.g., $.50, .50, $1.50, $.5, .5
        r'\b\$?(\d+)',           # e.g., $500, $5, 500, 5
        r'\b\$?(\d+\.?)',         # e.g., $5.
        r'\b\$?(\d{1,3},\d{3})*',           # e.g., $123,456, $1,234, $12,345
        r'\b\$?(\d{1,3},\d{3})*\.?',         # e.g., $123,456.5, $1,234, $12,345
        r'\b\$?(\d{1,3},\d{3})*\.\d{1,2}',         # e.g., $123,456.5, $1,234, $12,345
    ]))
    result = re.findall(money_regex, data)
    #print(f"test_money result: {result}")
    print(f"{test_string_contains_money.__name__} result: {result}")
    assert result
    assert result[0]
    assert re.match(money_regex, data)
    #print(f"match result: {re.match(money_regex, data)}")
    #assert expected == bool(re.match(money_regex, data))

STRING_PUNCTUATION_TEST_CASES = [
    ("Sky is blue.", ['Sky', 'is', 'blue', '.']),
    ("Leaves are green.", ['Leaves', 'are', 'green', '.']),
    ("Roses are red.", ['Roses', 'are', 'red', '.']),
    ("Very very long sentence...", ['Very', 'very', 'long', 'sentence', '...']),
    ("Last sentence .", ["Last", "sentence", "."])
]
@pytest.mark.parametrize("data, expected", STRING_PUNCTUATION_TEST_CASES)
def test_string_with_punctuation(data, expected):
    string_regex = re.compile('|'.join([
        r'(\w+)\s*([.,!?;]*)',
    ]))
    result = re.findall(string_regex, data)
    assert result
    list_result = [x for t in result for x in t if x]
    print(f"{test_string_with_punctuation.__name__} result: {result} {list_result}")
    assert result[0]
    assert re.match(string_regex, data)
    assert expected == list_result
