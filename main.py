from policy_graph import Node,Graph,LinearPolicyGraph,Scenario
import copy
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from model import AbstractSubproblem, make_state_var
from pyomo.environ import Binary, NonNegativeReals, Var, Param, Objective, Constraint, SolverFactory, Suffix


if __name__ == '__main__':
    lpg = LinearPolicyGraph({1: 'try'})
    stage_1_scn = [Scenario(name=str(i), data_object=None) for i in range(3)]
    stage_2_scn = [Scenario(name=str(i), data_object=None) for i in range(4)]

    m = AbstractSubproblem()
    m.X = make_state_var(within=NonNegativeReals, bounds=(0, 3))
    m.Y = Var(bounds=(0,1))
    m.Z = Var(bounds=(1,1))
    m.demand = Param(initialize=2)
    m.demand_supply = Constraint(expr=m.X+2*m.Y+1/2*m.Z >= m.demand)
    m.objective = Objective(expr=3*m.X+2*m.Y)

    lpg.add_stage(stage_1_scn)
    lpg.add_stage(stage_2_scn)
    lpg.add_stage(stage_2_scn)
    lpg.add_stage(stage_2_scn)

    lpg.assign_subproblem(m)

    lpg.summary()
    lpg.display()
    input()
