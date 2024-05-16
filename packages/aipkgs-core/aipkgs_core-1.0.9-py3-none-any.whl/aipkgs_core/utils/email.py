from email_validator import validate_email, EmailNotValidError


def is_email_valid(email: str,
                   allow_smtputf8: bool = False,
                   check_deliverability: bool = False,
                   allow_empty_local: bool = False
                   ) -> (bool, str):
    try:
        valid = validate_email(email,
                               allow_smtputf8=allow_smtputf8,
                               check_deliverability=check_deliverability,
                               allow_empty_local=allow_empty_local)

        email = valid.email
        return True
    except EmailNotValidError as e:
        return False


def is_valid_email(email: str,
                   allow_smtputf8: bool = False,
                   check_deliverability: bool = False,
                   allow_empty_local: bool = False
                   ) -> bool:
    return is_email_valid(email,
                          allow_smtputf8=allow_smtputf8,
                          check_deliverability=check_deliverability,
                          allow_empty_local=allow_empty_local)