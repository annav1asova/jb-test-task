def is_alpha(sym):
    return 'a' <= sym <= 'z'


def is_digit(sym):
    return '0' <= sym <= '9'


def is_allowed_special(sym):
    return sym == ' ' or sym == "\""
