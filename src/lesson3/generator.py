from collections import frozenset

null = frozenset()


def lit(s):
    set_s = set([s])
    return lambda lengths: set_s if len(s) in lengths else null

def alt(x, y):
    return lambda lengths: x(lengths) | y(lengths)

def oneof(chars):
    set_chars = set(chars)
    return lambda lengths: set_chars if 1 in lengths else null

def star(x):
    return lambda lengths: opt(plus(x))(lengths)


def plus(x):
    return lambda lengths: genseq(x, star(x), lengths, startx=1)


def seq(x, y):
    return lambda lengths: genseq(x, y, lengths)


# seq(x, y) return a function fn(lengths) that returns a set of texts the
# match. It delays calculations.
# genseq(x, y, lengths) returns the set of texts.


def genseq(x, y, lengths, startx=0):
    """Set of matches to xy whose total len is in lengths...
    Tricky point: x+ is defined as x+ = xx*
    To stop the recursion, the first x must generate at least 1 character,
    and then the recursive x* has that many fewer characters. We use startx=1
    to say that x must match at least 1 character.
    """
    if not lengths:
        return null
    xmatches = x(set(range(startx, max(lengths) + 1)))
    ns_x = set(len(m) for m in xmatches)
    ns_y = set(n - m for n in lengths for m in ns_x if n - m >= 0)
    ymatches = y(ns_y)
    return set(m1 + m2
               for m1 in xmatches for m2 in ymatches
               if len(m1 + m2) in lengths)


dot = oneof('?')
epsilon = lit('')  # Std name in Language Theory for empty strings.
