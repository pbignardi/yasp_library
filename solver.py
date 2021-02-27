from pyomo.environ import SolverFactory
from policy_graph import Node, Graph


class Solver:
    def __init__(self):
        pass

    @staticmethod
    def __forward_simulation(graph: Graph, state_variables: list):
        trial_solution = dict()

