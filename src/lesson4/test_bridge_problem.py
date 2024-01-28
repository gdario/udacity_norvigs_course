import unittest
import bridge_problem as bp


class TestBridgeProblem(unittest.TestCase):
    def test_two_solutions(self):
        sol1 = [(2, 1, '->'), (1, 1, '<-'), (5, 10, '->'), (2, 2, '<-'),
                (2, 1, '->')]
        sol2 = [(2, 1, '->'), (2, 2, '<-'), (5, 10, '->'), (1, 1, '<-'),
                (2, 1, '->')]
        sol = bp.bridge_problem([1, 2, 5, 10])
        self.assertTrue(bp.path_actions(sol) in (sol1, sol2))
