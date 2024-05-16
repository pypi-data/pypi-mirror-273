from email_validator import validate_email, EmailNotValidError, ValidatedEmail

from aipkgs_core.utils import utils


def is_email_valid(email: str,
                   allow_smtputf8: bool = False,
                   check_deliverability: bool = False,
                   allow_empty_local: bool = False
                   ) -> (bool, str):
    try:
        if utils.contains_extra_spaces(email):
            return False

        validated_email: ValidatedEmail = validate_email(email,
                                                         allow_smtputf8=allow_smtputf8,
                                                         check_deliverability=check_deliverability,
                                                         allow_empty_local=allow_empty_local)

        email = validated_email.ascii_email
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
