from num2words import num2words


def dollars2words(f):
    d, dot, cents = f.partition(".")
    return "{dollars}{cents}".format(
        dollars=num2words(int(d)),
        cents=" and {}/100 cents".format(cents)
        if cents and int(cents)
        else "",
    )
