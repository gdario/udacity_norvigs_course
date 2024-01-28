def bsuccessors(state):
    """Return a dict of {state: action} pairs. A state is a (here, there, t)
    tuple, where here and there are frozensets of people (indicated by their
    times) and/or the 'light', and t is a number indicating the elapsed time.
    Action is represented by '->' for here to there and '<-' for there to
    here."""
    here, there, t = state
    if 'light' in here:
        return dict(((here - frozenset([a, b, 'light']),
                      there | frozenset([a, b, 'light']),
                      t + max(a, b)),
                     (a, b, '->'))
                    for a in here if a != 'light'
                    for b in here if b != 'light')
    else:
        return dict(((here | frozenset([a, b, 'light']),
                      there - frozenset([a, b, 'light']),
                      t + max(a, b)),
                     (a, b, '<-'))
                    for a in there if a != 'light'
                    for b in there if b != 'light')


def path_states(path):
    """Return a list of states in this path.
    Paths are [state, action, state, action, state]
    """
    # States are the even-numbered positions.
    return path[0::2]


def path_actions(path):
    """Return a list of actions in this path.
    Paths are [state, action, state, action, state]
    """
    # States are the odd-numbered positions.
    return path[1::2]


def bridge_problem(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()  # set of states we have visited
    frontier = [[(here, frozenset(), 0)]]
    if not here:
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        here1, there1, t1 = state1 = path[-1]
        if not here1 or here1 == set(['light']):
            return path
        for (state, action) in bsuccessors(state1).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                frontier.append(path2)
                frontier.sort(key=elapsed_time)
    return []


def elapsed_time(path):
    "Return the total elapsed time associated with a path."
    return path[-1][2]


def main():
    start = (frozenset((1, 2, 5, 10, 'light')), frozenset(), 0)
    print(bridge_problem(start[0]))


main()
