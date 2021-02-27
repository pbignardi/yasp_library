# Build the policy graph of the problem. This can be built using a node+edge structure, defining the whole tree.
import networkx as nx
import numpy as np
from typing import List
from utils import Toolbox
from random import choice, seed
import matplotlib.pyplot as plt


# Scenario object, use dict or DataPortal
class Scenario(object):
    def __init__(self, name, data_object):
        self.name = name
        self.data = data_object

    def __repr__(self):
        return f"Scenario(name: {self.name}, data: {self.data})"

    def __str__(self):
        return f"{self.name}"


# Node object, construct a node, with specific scenario and probability
class Node(object):
    def __init__(self, name: str, scn, p, parent=None):
        # Unpacking singleton
        if type(scn) == list:
            if len(scn) == 1:
                scn, = scn
        if type(p) == list:
            if len(p) == 1:
                p, = p

        # Initialization
        self.name = name
        self.parent: Node = parent
        self.scenario = scn
        self.p = p

        # Validate input
        if self.is_stochastic:
            assert type(self.p) == list
            assert len(self.scenario) == len(self.p)
            assert Toolbox.is_density(self.p)
        else:
            assert Toolbox.is_probability(self.p)

    @property
    def parent_type(self):
        return type(self.parent)

    @property
    def is_stochastic(self):
        return type(self.scenario) == list and len(self.scenario) > 1

    @property
    def get_name_list(self):
        if self.is_stochastic:
            name_list = [self.name + '_' + scn.name
                         for scn in self.scenario]
            return name_list
        else:
            return self.name

    @property
    def type(self):
        return 'Node' if not self.is_stochastic else 'Stochastic'

    def get_rnd_scenario(self, s=0):
        seed(s)
        if self.is_stochastic:
            return choice(self.scenario)
        else:
            return self.scenario


# Tree object, to represent the scenarios in the decision-making process.
class Graph(object):
    def __init__(self, root_scenario):
        # root node is deterministic, no scenario is necessary.
        self._root = Node('root', root_scenario, 1.0)
        self._nx_graph = nx.DiGraph()
        self._nx_graph.add_node('root',
                                data=self._root.scenario,
                                type=self._root.type,
                                p=self._root.p,
                                names=self._root.get_name_list)
        self._assignment_dict = dict()

    @property
    def nodes(self):
        return self._nx_graph.nodes

    @property
    def graph(self):
        return self._nx_graph

    @property
    def assignment_map(self):
        return self._assignment_dict

    @property
    def assigned_nodes(self):
        return self.assignment_map.keys()

    @assignment_map.setter
    def assignment_map(self, assign_dict):
        self._assignment_dict = assign_dict

    @property
    def unassigned_nodes(self):
        return [node for node in self.nodes if node not in self.assigned_nodes]

    def assign(self, abstract_problem, node_name):
        self._assignment_dict[node_name] = abstract_problem

    def display(self):
        nx.draw_networkx(self._nx_graph, with_labels=True, arrows=True)
        plt.show()

    def summary(self):
        for node_name in self.nodes:
            node = self.graph.nodes[node_name]
            print(f"Node name: {node_name} \t ",
                  f"Node Type: {node['type']} \t ",
                  f"Scenarios: {str(node['data'])} \t ",
                  f"Probability: {node['p']}")
        print(f"Stages: {len(nx.dfs_successors(self.graph,source='root'))+1}")

    def add_node(self, node: Node):
        # Check if name is already contained:
        node_names = list(self._nx_graph.nodes.keys())
        if node.name in node_names:
            raise Exception(f"Node name {node.name} already exists in the scenario tree!")

        # Add node
        self._nx_graph.add_node(node.name,
                                data=node.scenario,
                                type=node.type,
                                p=node.p,
                                names=node.get_name_list)
        if node.parent is not None:
            self.add_edge(node.parent.name, node.name, node.p)

    def add_edge(self, start_name: str, finish_name: str, probability: np.float64):
        self._nx_graph.add_edge(start_name, finish_name, p=probability)

    def get_children_name(self, parent_name: str) -> List[str]:
        return list(self._nx_graph.successors(parent_name))

    def get_parent_name(self, child_name: str) -> str:
        parent: str = list(self._nx_graph.predecessors(child_name))[0]
        return parent


# Construct a linear policy graph by adding nodes with scenarios one at a time
class LinearPolicyGraph(Graph):
    def __init__(self, root_scenario):
        super().__init__(root_scenario)
        self.__last_t: int = 1
        self.__last_node = self._root
    
    @property
    def num_stages(self):
        return self.__last_t

    # Create stage with the scenario list provided
    #   kwargs:
    #       prob_list = list of probabilities for provided list of scenarios
    def add_stage(self, scenario_list: list, **kwargs):
        n = len(scenario_list)
        prob_list = [1 / n for _ in range(n)]

        if 'prob_list' in kwargs:
            prob_list = kwargs['prob_list']

        self.__last_t += 1
        stage_node = Node(f"stage_{self.__last_t}",
                          scn=scenario_list,
                          p=prob_list,
                          parent=self.__last_node)
        self.add_node(stage_node)
        self.__last_node = stage_node

    def assign_subproblem(self, abstract_model):
        for node_name in self.nodes:
            self.assign(abstract_model, node_name)




