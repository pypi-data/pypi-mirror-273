import phonenumbers
from phonenumbers import PhoneNumber

from aipkgs_core.utils import utils


def is_number_format_valid(number: str) -> (bool, str):
    try:
        # if utils.contains_space(number):
        #     return False, number

        parsed_number: PhoneNumber = phonenumbers.parse(number, None)
        return True, parsed_number
    except:
        return False, number


def is_valid_full_number(number: str) -> (bool, PhoneNumber):
    is_valid, phone_number = is_number_format_valid(number)
    if not is_valid:
        return False, phone_number
    is_phone_valid = phonenumbers.is_valid_number(phone_number)
    return is_phone_valid, phone_number


def is_valid_number_with_country_code(country_code: str, national_number: str) -> (bool, PhoneNumber):
    full_number = f"+{country_code}{national_number}"
    return is_valid_full_number(full_number)
