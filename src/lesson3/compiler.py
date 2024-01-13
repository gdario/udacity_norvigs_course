from collections import frozenset

null = frozenset()


def match(pattern, text):
    "Match pattern against start of text. Return longest match found or None."
    remainders = pattern(text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text)-len(shortest)]


def search(pattern, text):
    "Match pattern anywhere in text. Return longest earliest match or none."
    for i in range(len(text)):
        m = match(pattern, text[i:])
        if m is not None:  # The empty string counts as false, but we want it.
            return m


def lit(s):
    return lambda text: set([text[len(s):]]) if text.startswith(s) else null


def seq(x, y):
    return lambda text: set().union(*map(y, x(text)))


def alt(x, y):
    return lambda text: x(text) | y(text)


def oneof(chars):
    return lambda t: set([t[1:]]) if (t and t[0] in chars) else null


def plus(x):
    return (x, star(x))


def opt(x):
    return alt(list(''), x)


def star(x):
    return lambda text: (set([text]) |
                         set(t2 for t1 in x(t) if t1 != t
                             for t2 in star(x)(t1)))


dot = lambda text: set([text[1:]]) if text else null
eol = lambda text: set(['']) if text == '' else null

