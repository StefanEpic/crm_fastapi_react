from string import punctuation


def name_valid(name: str) -> str:
    """
    Name validations
    :param name: string
    :return: string
    """
    if not name.isalpha():
        raise ValueError("Error. Invalid value for name field")
    return name


def email_valid(email: str) -> str:
    """
    Email validations
    :param email: string
    :return: string
    """
    if "@" not in email:
        raise ValueError("Error. Invalid value for email field")
    return email


def phone_valid(phone: str) -> str:
    """
    Phone number validations
    :param phone: string
    :return: string
    """
    p = punctuation.replace("+", "")
    if phone.isalpha() or len(set(p) & set(phone)) > 0:
        raise ValueError("Error. Invalid value for phone field")
    return phone
