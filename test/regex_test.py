import pytest, logging, os, re
def test_numnerRegex():
    numberRegex = r"^(\d)+$"
    assert re.match(numberRegex, "123")
    assert not re.match(numberRegex, "Hello World")
    assert not re.match(numberRegex, "123 ")
    assert not re.match(numberRegex, " 123")
    assert not re.match(numberRegex, "123.")
    assert not re.match(numberRegex, "123-")

def test_stringRegex():
    regex = r"^([\w\d\-_\s])+$"
    assert re.match(regex, "Hello World")
    assert re.match(regex, "Hello-World")
    assert re.match(regex, "Hello_World")
    assert re.match(regex, "Hello World 123")
    assert not re.match(regex, "Hello World!!!")
    assert not re.match(regex, "Hello World ~!@#$%^&*()_+")

def test_stringRegexMax():
    regexMax = r"^([\w\d\-_\s]){5,10}$"
    assert re.match(regexMax, "Hello-Worl")
    assert re.match(regexMax, "Hello_Worl")
    assert re.match(regexMax, "HelloWorl8")
    assert not re.match(regexMax, "Helo")
    assert not re.match(regexMax, "HelloWorl89")
    assert not re.match(regexMax, "Hello World ~!@#$%^&*()_+")

def test_lettersRegex():
    lettersRegex = r"^([a-zA-Z]){0,10}$"
    assert re.match(lettersRegex, "HelloWorld")
    assert not re.match(lettersRegex, "HelloWorl0") # Should NOT match due to number
    assert not re.match(lettersRegex, "Hello Worl") # Should NOT match due to space
    assert not re.match(lettersRegex, "Hello World") # Should NOT match due to length

def test_emailRegex():
    emailRegex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    assert not re.match(emailRegex, "")
    assert not re.match(emailRegex, ".@.")
    assert not re.match(emailRegex, "-@-")
    assert not re.match(emailRegex, "a@")
    assert not re.match(emailRegex, "a@b")
    assert not re.match(emailRegex, "ab@de")
    assert not re.match(emailRegex, "abc@def")
    assert not re.match(emailRegex, "a@b.c")
    assert not re.match(emailRegex, "~!@#$%^&*()_+@b.c")
    assert not re.match(emailRegex, "~!#$%^&*()_+@b.c")
    assert not re.match(emailRegex, "kokhow.teh@b.c")
    assert not re.match(emailRegex, "kokhow teh@b.c")
    assert not re.match(emailRegex, "kok-how_teh@b.c")
    assert not re.match(emailRegex, "kok-how_teh@b.c.d")
    assert not re.match(emailRegex, "123@456")
    assert re.match(emailRegex, "123@ntu.edu.sg")
    assert re.match(emailRegex, "me@gmail.com")
    assert re.match(emailRegex, "tan_k_h@gmail.com")
    assert re.match(emailRegex, "tan-k.h@gmail.com")
    assert re.match(emailRegex, "tan-k.h@gmail.co.uk")
    assert not re.match(emailRegex, "tan k h@gmail.com")

def test_numericRegex():
    regex = r"^(\d{8,10})$"
    assert not re.match(regex, "1234567")
    assert re.match(regex, "12345678")
    assert re.match(regex, "123456789")
    assert re.match(regex, "1234567890")
    assert not re.match(regex, "12345678901")

def test_phoneNumberRegex():
    # 91234567, +123-1234567890
    phoneRegex = r"^(\+\d{1,3}\-?)*(\d{8,10})$"
    assert not re.match(phoneRegex, "1234567") # Invalid due to length < 8
    assert re.match(phoneRegex, "12345678")
    assert re.match(phoneRegex, "1234567890")
    assert not re.match(phoneRegex, "12345678901") # Invalid due to length > 10
    assert re.match(phoneRegex, "+6512345678")
    assert re.match(phoneRegex, "+65-12345678")
    assert not re.match(phoneRegex, "+ab-91234567")
    assert not re.match(phoneRegex, "+65 91234567") # Invalid due to space
    assert not re.match(phoneRegex, "+123-1234567") # Invalid due to length < 8
    assert re.match(phoneRegex, "+123-12345678")
    assert re.match(phoneRegex, "+123-1234567890")
    assert not re.match(phoneRegex, "+123-12345678901") # Invalid due to length > 10
    assert not re.match(phoneRegex, "+-1234567890") # Invalid due to country code < 1
    assert not re.match(phoneRegex, "-1234567890") # Invalid due to country code < 1
    assert not re.match(phoneRegex, "+1234-1234567890") # Invalid due to country code > 3
    assert not re.match(phoneRegex, "+123-HelloWorld")
    assert not re.match(phoneRegex, "+123-")