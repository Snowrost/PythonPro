import pytest
from regexhm import passport, uin, car_in


def test_valid_passport():
    assert passport("AB123456") == "Valid passport number"
    assert passport("КМ123456") == "Valid passport number"


def test_invalid_passport():
    assert passport("12345") == "Invalid passport number"
    assert passport("КМ12345") == "Invalid passport number"
    assert passport("К123456") == "Invalid passport number"


def test_valid_uin():
    assert uin("1234567890") == "Valid uin number"


def test_invalid_uin():
    assert uin("12345") == "Invalid uin number"

def test_car_region():
    assert car_in("АХ5563АП") == "Kharkiv Region"
    assert car_in("ІІ5563АП") == "Invalid Car Number"
    assert car_in("АЕ5563АП") == "Dnipro Region"



