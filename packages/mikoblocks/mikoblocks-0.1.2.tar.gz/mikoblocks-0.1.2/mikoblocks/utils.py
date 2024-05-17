import re

def _is_valid_tag_name(tag_name: str) -> bool:
    """ Validate if the string can be a valid HTML tag name. """
    # HTML tags consist of alphanumeric characters and dashes.
    # They must start with a letter and cannot only be digits or dashes.
    return bool(re.match(r'^[A-Za-z][A-Za-z0-9\-]*$', tag_name))