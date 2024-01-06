from string import punctuation


def name_valid(name: str) -> str:
    """
    Name validations
    :param name: name field
    :return: valid name
    """
    if not name.isalpha():
        raise ValueError("Invalid value for family, name or surname fields")
    return name.capitalize()


def phone_valid(phone: str) -> str:
    """
    Phone validations
    :param phone: phone number field
    :return: valid phone number
    """
    p = punctuation.replace("+", "")
    if phone.isalpha() or len(set(p) & set(phone)) > 0:
        raise ValueError("Invalid value for phone field")
    return phone
