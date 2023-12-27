from collections import defaultdict

def test_shuffler(shuffler, dec='abcd', n=10000):
    counts = defaultdict(int)
    for _ in range(n):
        input = list(deck)
        shuffler(input)
        counts[''.join(input)] += 1
    e = n*1./factorial(len(deck))
    ok = all((0.9 <= counts[item]/e <= 1.1) for item in counts)
    name = shuffler.__name__
    print('%s(%s) %s' % (name, deck, ('ok' if ok else '*** BAD ***')))
    print()
    for item, count in sorted(counts.items()):
        print('%s:%4.1f' % (item, count*100./n))
    print()


def test_shufflers(shufflers=[shuffle, shuffle1], decks=['abc', 'ab']):
    for deck in decks:
        print()
        for f in shufflers:
            test_shuffler(f, deck)

def factorial(n):
    return 1 if (n <= 1) else n*factorial(n-1)


def shuffle2(deck):
    "A modification of the teacher's algorithm."
    n = len(deck)
    swapped = [False] * n
    while not all(swapped):
        i, j = random.randrange(n), random.randrange(n)
        swapped[i] = True
        swap(deck, i, j)


def shuffle3(deck):
    "An easier modification of the teacher's algorithm."
    n = len(deck)
    for i in range(n):
        swap(deck, i, random.randrange(n))
