from typing import NamedTuple

import bcrypt


class PasswordHash(NamedTuple):
    hash: str
    salt: str


def hash_password(password: str) -> PasswordHash:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Return the hashed password as a utf-8 encoded string
    return PasswordHash(hashed_password.decode('utf-8'), salt.decode('utf-8'))


def check_password(password: str, hashed_password: str) -> bool:
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def contains_extra_spaces(s: str) -> bool:
    return '  ' in s


def remove_extra_spaces(s: str) -> str:
    return ' '.join(s.split())


def remove_substring(s: str, substring: str) -> str:
    return s.replace(substring, '')
