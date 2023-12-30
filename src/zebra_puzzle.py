import itertools


def imright(h1, h2):
    "House h1 is immediately right of h2 if h1 - h2  == 1."
    return h1 - h2 == 1


def nextto(h1, h2):
    "Two houses are next to each other if they differ by 1."
    return abs(h1 - h2) == 1


def zebra_puzzle():
    "Return a tuple (WATER, ZEBRA) indicationg their house numbers."
    houses = first, _, middle, _, _ = [1, 2, 3, 4, 5]
    # The numbers below represent the constraints to the problem.
    # Returns the first (WATER, ZEBRA) tuple that satisfies all contraints.
    orderings = list(itertools.permutations(houses))  # 1
    return next((WATER, ZEBRA)
                for (red, green, ivory, yellow, blue) in c(orderings)
                if imright(green, ivory)          # 6
                for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in c(orderings)
                if Englishman is red              # 2
                if Norwegian is first             # 10
                if nextto(Norwegian, blue)        # 15
                for (coffee, tea, milk, oj, WATER) in c(orderings)
                if coffee is green                # 4
                if Ukranian is tea                # 5
                if milk is middle                 # 9
                for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in c(orderings)
                if Kools is yellow                # 8
                if LuckyStrike is oj              # 13
                if Japanese is Parliaments        # 14
                for (dog, snails, fox, horse, ZEBRA) in c(orderings)
                if Spaniard is dog                # 3
                if OldGold is snails              # 7
                if nextto(Chesterfields, fox)     # 11
                if nextto(Kools, horse))          # 12


def instrument_fn(fn, *args):
    # c.starts counts the number of times we start iterating over orderings
    # c.items counts the number of times we go through a loop
    breakpoint()
    c.starts, c.items = 0, 0
    result = fn(*args)
    print(f'{fn.__name__} got {result} with {c.starts:05} iterations over {c.items:07} items')


def c(sequence):
    """Generate items in sequence, keeping counts as we go. c.starts is the number of sequences started. c.items is the number of items generated."""
    c.starts += 1
    for item in sequence:
        c.items += 1
        yield item

print(instrument_fn(zebra_puzzle))
# if __name__ == '__main__':
#     print(instrument_fn(zebra_puzzle))
