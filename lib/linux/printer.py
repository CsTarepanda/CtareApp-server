COLOR_SPACE = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]


def _color_get_place(byte_1):
    if byte_1 == 0xff:
        return 5
    for index, i in enumerate(COLOR_SPACE):
        if i > byte_1:
            return index - (1 if byte_1 - COLOR_SPACE[index - 1] <= i - byte_1 else 0)


def color(byte_3):
    if byte_3%0xa0a0a == 0x80808:
        return 232 + int((byte_3 - 0x080808) / 0xa0a0a)
    pos = 16
    for i in range(3):
        pos += _color_get_place(byte_3 & 0xff) * 6**i
        byte_3 >>= 8
    return pos


def mkcl(color_num):
    return "[38;5;{}m".format(color_num)


def mkclb(color_num):
    return "[48;5;{}m".format(color_num)


def cstr(string, col):
    return "{0}{1}{2}[0m".format(col[0], col[1], string)


def cprint(string, col):
    print(cstr(string, col))


def inprint(string):
    print("[s\n[u[F[L{}[u".format(string), end="")
