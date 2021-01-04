""" Collection of string processing functions """


def safe_filename(string, special="._"):
    """ Return a safe verison of string for a file """
    string = string.strip().lower().replace(" ", "_")
    return "".join([c for c in string if c.isalnum() or c in special])
