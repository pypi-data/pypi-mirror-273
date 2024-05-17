class ConvertError(Exception):
    ...


class Style:
    BRIGHT = '\033[1m'
    NORMAL = '\033[22m'
    BACK_WHITE = '\033[7m'
    UNDER = '\033[4m'
    RESET = '\033[0;0m'

    BLACK = '\033[30m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[1;34m'
    MAGENTA = '\033[1;35m'
    CYAN = '\033[1;36m'
    WHITE = '\033[1;37m'

    LIGHT_BLACK = '\033[1;90m'
    LIGHT_RED = '\033[1;91m'
    LIGHT_GREEN = '\033[1;92m'
    LIGHT_YELLOW = '\033[1;93m'
    LIGHT_BLUE = '\033[1;94m'
    LIGHT_MAGENTA = '\033[1;95m'
    LIGHT_CYAN = '\033[1;96m'
    LIGHT_WHITE = '\033[1;97m'


class Back:
    RED = '\033[41m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
