# -----------
# User Instructions
# 
# Define a function, two_pair(ranks).
import random

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']


def deal(numhands, n=5, deck=mydeck):
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]


def poker(hands):
    "Return the best hand: poker([hand,...]) => hand"
    return allmax(hands, key=hand_rank)


def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    max_rank = max(key(hand) for hand in iterable)
    return list(filter(lambda x: key(x) == max_rank, iterable))

############################################################################
#                        Initial version of hand_rank
############################################################################

# def hand_rank(hand):
#     ranks = card_ranks(hand)
#     if straight(ranks) and flush(hand):            # straight flush
#         return (8, max(ranks))
#     elif kind(4, ranks):                           # 4 of a kind
#         return (7, kind(4, ranks), kind(1, ranks))
#     elif kind(3, ranks) and kind(2, ranks):        # full house
#         return (6, kind(3, ranks), kind(2, ranks))
#     elif flush(hand):                              # flush
#         return (5, ranks)
#     elif straight(ranks):                          # straight
#         return (4, max(ranks))
#     elif kind(3, ranks):                           # 3 of a kind
#         return (3, kind(3, ranks), ranks)
#     elif two_pair(ranks):                          # 2 pair
#         return (2, two_pair(ranks))
#     elif kind(2, ranks):                           # kind
#         return (1, kind(2, ranks), ranks)
#     else:                                          # high card
#         return (0, ranks)
# 

############################################################################
#                  Second version, based on group and unzip
############################################################################

# def hand_rank(hand):
#     """Counts the count of each rank; ranks lists corresponding ranks
#     e.g., '7 T 7 9 7' => counts = (3, 1, 1)l ranks = (7, 10, 9)"""
#     groups = group(['--23456789TJQKA'.index(r) for r, s in hand])
#     counts, ranks = unzip(groups)
#     if ranks == (14, 5, 4, 3, 2):
#         ranks = (5, 4, 3, 2, 1)
#     straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
#     flush = len(set([s for r, s in hand])) == 1
#     return (9 if (5,) == counts else
#             8 if straight and flush else
#             7 if (4, 1) == counts else
#             6 if (3, 2) == counts else
#             5 if flush else
#             4 if straight else
#             3 if (3, 1, 1) == counts else
#             2 if (2, 2, 1) == counts else
#             1 if (2, 1, 1, 1) == counts else
#             0), ranks


# This dictionary maps the partition of 5 to the scores associated with
# the various hand types.
count_rankings = {(5,): 10, (4, 1): 7, (3, 2): 6, (3, 1, 1): 3,
                  (2, 2, 1): 2, (2, 1, 1, 1): 1, (1, 1, 1, 1, 1): 0}

############################################################################
#                  Version based on count_rankings
############################################################################

def hand_rank(hand):
    "Return a valu indicating how high the hand ranks."
    # Counts the count of each rank; ranks lists correspoinding ranks
    # e.g. '7 T 7 9 7' => counts = (3, 1, 1); ranks = (7, 10, 9)
    groups = group(['--23456789TJQKA'.index(r) for r, s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r, s in hand])) == 1
    return max(count_rankings[counts], 4*straight + 5*flush), ranks


def group(items):
    """Return a list of [(count, x)...], hight count first, then highest
    x first."""
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)


def unzip(pairs):
    return zip(*pairs)


def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse=True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks


def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return (max(ranks) - min(ranks) == 4) and len(set(ranks)) == 5


def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r, s in hand]
    return len(set(suits)) == 1


def two_pair(ranks):
    """If there are two pair here, return the two ranks of the two pairs,
    else None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None


def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r 
    return None


def hand_percentages(n=700_000):
    """Sample random hands and print a table of percentages for each type
    of hand."""
    counts = [0]*9
    for i in range(n//10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print("%14s: %6.3f %%" % (hand_names[i], 100.*counts[i]/n))


def test():
    "Test cases for the functions in poker program."
    sf1 = "6C 7C 8C 9C TC".split() # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "TD 9H TH 7C 3S".split() # Two Pair
    s1 = "AS 2S 3S 4S 5C".split() # A-5 straight
    s2 = "2C 3C 4C 5S 6S".split() # 2-6 straight
    ah = "AS 2S 3S 4S 6C".split() # Ace high
    sh = "2S 3S 4S 6C 7D".split() # 7 high
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) is None
    assert kind(2, fkranks) is None
    assert kind(1, fkranks) == 7
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2]
    return 'tests pass'


print(test())
