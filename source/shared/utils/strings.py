from re import finditer
from re import IGNORECASE
from re import match
from re import search


def after(string, substring):
    """ Returns the text after the search string
        Or returns the whole string if not found.
    """
    if string is None or substring is None:
        return string

    index = string.find(substring)

    if index == -1:
        return string

    return string[index + len(substring):]


def append(base_string, append_string, separator):
    """ Safely appends a string to the end of another string.
        If the base string is empty, will only return the append string.
        Otherwise it will return the base string + separator + append string.
    """
    if base_string:
        return base_string + separator + append_string

    return append_string


def before(string, substring):
    """ Returns the text before the search string
        Or returns the whole string if not found.
    """
    if string is not None and substring is not None:
        index = string.find(substring)
    else:
        index = -1

    if index > -1:
        return string[:index]
    else:
        return string


def contains(string, substring):
    """ None safe check if a string contains another string. """
    if string is not None and substring is not None:
        return (string.find(substring)) > -1
    elif substring is None:
        return True
    else:
        return False


def contains_ignore_case(string, substring):
    """ None safe check if a string contains another string. """
    if string is not None and substring is not None:
        return (string.lower().find(substring.lower())) > -1
    elif substring is None:
        return True
    else:
        return False


def ends_with(string, end_string):
    """ None safe check to see if a string ends in another string. """
    if string is not None and end_string is not None:
        return string.endswith(end_string)
    elif end_string is None:
        return True
    else:
        return False


def ends_with_ignore_case(string, end_string):
    """ None safe check to see if a string ends in another string. """
    if string is not None and end_string is not None:
        return string.lower().endswith(end_string.lower())

    if end_string is None:
        return True

    return False


def equals_ignore_case(string1, string2):
    """ Compare strings ignoring case.
        None safe.
        None == None -> True
    """
    if string1 is not None and string2 is not None:
        return string1.lower() == string2.lower()

    if string1 is None and string2 is None:
        return True

    # One is None but not both.
    return False


def find(string, pattern):
    result = search(pattern, string)
    if result:
        return result.group()
    return ''


def find_all(string, pattern):
    return [item.group() for item in finditer(pattern, string)]


def find_and_strip(string, pattern):
    return find(string, pattern).strip()


def find_indexes(string, pattern):
    """ Returns the starting location index
        for all matches in the string.
    """
    return [result.start() for result in finditer(pattern, string)]


def is_blank(text):
    if not text or text.isspace():
        return True
    return False


def is_comment(text):
    if is_empty(text):
        return False
    return text.lstrip().startswith('#') or text.lstrip().startswith('//')


def is_empty(text):
    if not text:
        return True
    return False


def is_shorter(new, original):
    return len(new) < len(original)


def join(strings, separator):
    """ Convenience function for joining a list of strings with a separator between items. """
    return separator.join(strings)


def lower(text):
    """ None safe string to lowercase function. """

    if text is not None:
        return text.lower()
    return text


def not_blank(text):
    return not is_blank(text)


def not_empty(text):
    return not is_empty(text)


def not_ends_with(string, end_string):
    return not ends_with(string, end_string)


def not_ends_with_ignore_case(string, end_string):
    return not ends_with_ignore_case(string, end_string)


def not_starts_with(string, start_string):
    return not starts_with(string, start_string)


def not_starts_with_ignore_case(string, start_string):
    return not starts_with_ignore_case(string, start_string)


def pad_difference(string, length, padding=' '):
    """ Returns the missing padding for the given string. """
    if len(string) >= length:
        return ''

    return padding * ((length - len(string)) // len(padding))


def replace(string, search_string, replace_string):
    """ None safe replace function.
        None returns None
        Also handles integers.
    """

    if string is None:
        return string

    # Change int to string:
    if isinstance(replace_string, int):
        replace_string = str(replace_string)

    # Replace:
    return string.replace(search_string, replace_string)


def starts_with(string, start):
    """ Null safe startswith function. """
    if string is not None:
        return string.startswith(start)

    return False


def starts_with_ignore_case(text, start):
    """ Null safe case insensitive startswith function. """
    if text:
        return bool(match(start, text, IGNORECASE))

    return False


def strip(string):
    """None safe string strip function.
       None returns None.
    """
    if string:
        return string.strip()

    return string
