import gurobipy as gp
from gurobipy import GRB, Model

class MasterProblem():
    def __init__(self):
        pass

    def solve(self):
        master_problem = Model("Master")

        x = master_problem.addVars(1, 2, 3, 4, vtype=GRB.CONTINUOUS)
        alpha = master_problem.addVar()

        master_problem.addConstr(
            x[1] +x[2] + 3* x[3] +x[4] >= 10,
        )
        master_problem.addConstr(
            x[1] + 3*x[2] + 5 * x[3] + 6 * x[4] >= 10,
        )
        master_problem.addConstr(
            alpha >= 0,
        )
        master_problem.addConstr(
            alpha >= 0,
        )
        #TODO: Figure out how to add the benders cuts as constraints






