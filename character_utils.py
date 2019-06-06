def is_alpha(sym):
    return sym >= 'a' and sym <= 'z'


def is_digit(sym):
    return sym >= '0' and sym <= '9'


def is_allowed_special(sym):
    return sym == ' ' or sym == "\""