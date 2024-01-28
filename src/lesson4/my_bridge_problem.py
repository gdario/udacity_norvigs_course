from collections import deque
import itertools as it


def my_bsuccessors(state):
    """Return a dict of {state: action} pairs. A state is a (here, there, t)
    tuple, where here and there are frozensets of people (indicated by their
    times) and/or the 'light', and t is a number indicating the elapsed time.
    Action is represented by '->' for here to there and '<-' for there to
    here."""
    here, there, t = state

    # If light in here send someone. If light in there someone comes back
    # state includes the total elapsed time.
    # Example: here = frozenset(1, 2, 5, 10, 'light'), there = frozenset()
    # state = (here, there, 0)
    # We may want to consider cases where 1 or 2 people cross the bridge.
    if 'light' in here:
        action = '->'
        fro, to = here, there
    else:
        action = '<-'
        fro, to = there, here

    fro = fro.difference({'light'})
    # Options are sending 1 or 2 people to the other side
    options = it.chain(it.combinations(fro, 1), it.combinations(fro, 2))
    if action == '->':
        return {(fro.difference(x), to.union(x).union({'light'}),
                 t + max(x)): action for x in options}
    else:
        return {(to.union(x).union({'light'}), fro.difference(x),
                 t + max(x)): action for x in options}


def my_failed_solver(start, goal):
    """We want the solver to return **all** solutions."""
    # If the 'there' configuration is the same as the goal, just return it.
    if start[1] == goal:
        return start
    # breakpoint()
    frontier = deque([[start]])
    explored = set()
    solutions = []
    while frontier:
        path = frontier.popleft()
        current = path[-1]
        for state, action in bsuccessors(current).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if goal == state[1]:
                    solutions.append(path2)
                else:
                    frontier.append(path2)
    return solutions
