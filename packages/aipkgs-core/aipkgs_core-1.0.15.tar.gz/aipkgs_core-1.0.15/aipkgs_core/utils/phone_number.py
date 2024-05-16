import phonenumbers
from phonenumbers import PhoneNumber

from aipkgs_core.utils import utils


def is_number_format_valid(number: str) -> (bool, str):
    try:
        if utils.contains_extra_spaces(number):
            return False

        parsed_number = phonenumbers.parse(number, None)
        return True, parsed_number
    except:
        return False, number


def is_valid_number(number: str) -> bool:
    is_valid, phone_number = is_number_format_valid(number)
    if not is_valid:
        return False
    return phonenumbers.is_valid_number(phone_number)
