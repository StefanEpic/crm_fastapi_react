def name_valid(name: str) -> str:
    """
    Name validations
    :param name: string
    :return: string
    """
    if not name.isalpha():
        raise ValueError("Error. Invalid value for name field")
    return name.capitalize()
