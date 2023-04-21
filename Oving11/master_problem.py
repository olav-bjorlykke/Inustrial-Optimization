import gurobipy as gp
from gurobipy import GRB, Model


#TODO: Currently the Master_problem is being re-instantiated for every iteration in the benders algorithm. Refactor so that it instead only adds the new optimality constraint for ever iteration.

class MasterProblem:
    def __init__(self, y_values_1, y_values_2, sensitivities_1, sensitivities_2, prev_x_values):
        #Add values from all previous iterations of benders
        self.y_1 = y_values_1
        self.y_2 = y_values_2
        self.lamda = sensitivities_1
        self.pi = sensitivities_2
        self.x_prev = prev_x_values
        pass

    def solve(self):
        #Initialize model
        master_problem = Model("Master")

        #Declare variables
        x = master_problem.addVars(4, vtype=GRB.CONTINUOUS)
        alpha = master_problem.addVar()

        #Adding constraints from initial problem
        master_problem.addConstr(
            x[0] +x[1] + 3* x[2] +x[3] >= 10,
        )
        master_problem.addConstr(
            x[0] + 3*x[1] + 5 * x[2] + 6 * x[3] >= 10,
        )
        #Adding lower bound to alpha
        master_problem.addConstr(
            alpha >= 0,
        )

        #Adding benders optimality constraints
        for k in range(len(self.y_1)-1):
            master_problem.addConstr(
                alpha >=
                0.5 * (self.y_1[k][0] + 2* self.y_1[k][1] + 4 * self.y_1[k][2])  +
                0.5 * (self.y_2[k][0] + 2 * self.y_2[k][1] + 4 * self.y_2[k][2]) +
                gp.quicksum((self.lamda[k][j] + self.pi[k][j])*(x[j] - self.x_prev[k][j]) for j in range(len(self.lamda[k])))
            )

        #Declaring objective function
        objective = x[0] + 4 * x[1] + 2 * x[2] + 5 * x[3] + alpha
        master_problem.setObjective(objective, GRB.MINIMIZE)

        #Solving the model
        master_problem.optimize()

        #Prepare variables for printing
        x_values = [x[i].X for i in range(4)]
        objective_value = master_problem.ObjVal

        return x_values, objective_value









