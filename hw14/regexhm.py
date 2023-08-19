import re


def passport(passport_number):
    passport_pattern = re.compile(r'^[А-ЯA-Z]{2}\d{6}$')
    if re.match(passport_pattern, passport_number):
        return "Valid passport number"
    else:
        return "Invalid passport number"


def uin(uin_number):
    uin_pattern = re.compile(r'^\d{10}$')
    if re.match(uin_pattern, uin_number):
        return "Valid uin number"
    else:
        return "Invalid uin number"


def car_in(car_number):
    car_number_pattern = re.compile(r'^А[ЕХ]\d{4}[А-Я]{2}$')
    if car_number_pattern.match(car_number):
        region_code = car_number[:2]
        if region_code == "АХ":
            return "Kharkiv Region"
        else:
            return "Dnipro Region"
    else:
        return "Invalid Car Number"
