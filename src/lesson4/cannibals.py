from pprint import pprint


def add(x, y):
    """Add two tuples and return the result only if there are no negative values.

    Args:
        x (tuple): A tuple.
        y (tuple): Another tuple.

    Returns:
        tuple or None: either the element-wise sum of the two tuples, or None.
    """
    res = tuple(x+y for x, y in zip(x, y))
    if none_negative(res):
        return res


def sub(x, y):
    res = tuple(x-y for x, y in zip(x, y))
    if none_negative(res):
        return res


def csuccessors(state):
    """Compute the successors of the cannibals and missionaries problem.

    >>> csuccessors((3, 3, 1, 0, 0, 0)) 
    {(1, 3, 0, 2, 0, 1): 'mm->', (3, 1, 0, 0, 2, 1): 'cc->', (2, 2, 0, 1, 1, 1): 'mc->', (2, 3, 0, 1, 0, 1): 'm->', (3, 2, 0, 0, 1, 1): 'c->'}
    """
    m1, c1, b1, m2, c2, b2 = state
    if c1 > m1 > 0 or c2 > m2 > 0:
        return {}
    items = []
    if b1 > 0:
        items += [(sub(state, delta), a + '->')
                  for delta, a in deltas.items()
                  if sub(state, delta)]
    if b2 > 0:
        items += [(add(state, delta), '<-' + a)
                  for delta, a in deltas.items()
                  if add(state, delta)]
    return dict(items)


deltas = {(2, 0, 1, -2,  0, -1): 'mm',
          (0, 2, 1,  0, -2, -1): 'cc',
          (1, 1, 1, -1, -1, -1): 'mc',
          (1, 0, 1, -1,  0, -1): 'm',
          (0, 1, 1,  0, -1, -1): 'c'}


def none_negative(state):
    """Check that there are no negative numbers of missionaries, cannibals or 
    boats."""
    return all([x >= 0 for x in state])


def mc_problem(start=(3, 3, 1, 0, 0, 0), goal=None):
    if goal is None:
        goal = (0, 0, 0) + start[:3]
    if start == goal:
        return [start]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in csuccessors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if state == goal:
                    return path2
                else:
                    frontier.append(path2)
    return []


if __name__ == '__main__':
    import doctest
    from pprint import pprint
    doctest.testmod()
    pprint(mc_problem())
