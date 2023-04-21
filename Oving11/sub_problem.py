import gurobipy as gp
from gurobipy import GRB, Model

class SubProblem():
    def __init__(self):
        pass

    def solve(self):
        subproblem = Model("Subproblem")

        y = subproblem.addVars(1,2,3, vtype= GRB.CONTINUOUS)