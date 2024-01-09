# --------------
# User Instructions
#
# Modify the function compile_formula so that the function
# it returns, f, does not allow numbers where the first digit
# is zero. So if the formula contained YOU, f would return
# False anytime that Y was 0

import re
import itertools


def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found, as a str,
    in same order as parms of function. The first digit of a multi-digit 
    number can't be 0. So if YOU is a word in the formula, and the function
    is called with Y eqal to 0, the function should return False."""

    letters = ''.join(set(re.findall('[A-Z]', formula)))
    parms = ', '.join(letters)
    words = re.split('([A-Z]+)', formula)
    constraints = ' and  '.join(
        [f'{word[0]} != 0' for word in words
         if len(word) > 1 and word.isupper()])
    tokens = map(compile_word, words)
    body = ''.join(tokens)
    if constraints:
        f = f'lambda {parms}: {body}' + ' and ' + constraints
    else:
        f = 'lambda %s: %s' % (parms, body)
    if verbose:
        print(f)
    return eval(f), letters


def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words uncahanged: compile_word('+') => '+'"""
    if word.isupper():
        terms = [('%s*%s' % (10**i, d))
                 for (i, d) in enumerate(word[::-1])]
        return '(' + '+'.join(terms) + ')'
    else:
        return word


def faster_solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the formula; only one eval per formula."""
    f, letters = compile_formula(formula)
    for digits in itertools.permutations(
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 0), len(letters)):
        try:
            if f(*digits) is True:
                table = str.maketrans(letters, ''.join(map(str, digits)))
                return formula.translate(table)
        except ArithmeticError:
            pass


def test():
    # should NOT return '1 + 0 == 01'
    assert faster_solve('A + B == BA') == None
    # assert faster_solve('YOU == ME**2') == '576 == 24**2'
    assert faster_solve('X / X == X') == '1 / 1 == 1'
    return 'tests pass'


test()
