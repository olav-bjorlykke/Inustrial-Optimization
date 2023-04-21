import gurobipy as gp
from gurobipy import GRB, Model

#TODO: Currently the model creates a new instance of the subproblem object for every iteration. Refactor so that we keep the same model but can solve it with new x-values.
#TODO: Move the passing of the x_vector to the solve() function in the subproblem.

class SubProblem:
    def __init__(self, x_vector, subproblem_number):
        self.x_values = x_vector
        self.number = subproblem_number

    def solve(self):
        #Declaring the model
        subproblem = Model("Subproblem")

        #Adding variables
        y = subproblem.addVars(3, vtype= GRB.CONTINUOUS)
        x = subproblem.addVars(len(self.x_values), vtype= GRB.CONTINUOUS)

        if self.number == 1:
            #Adding constraints specific to subproblem 1
            pass
            subproblem.addConstr(
                2*x[0] - x[1] + 7* x[2] + 5*x[3] + 2*y[0] + y[1] + y[2] >= 40
            )
            subproblem.addConstr(
                3 * x[0] - 10* x[1] + 4 * x[2] + 1 * x[3] + 3 * y[0] - y[1] + y[2] >= 25
            )

        if self.number == 2:
            #Adding constraints specific to subproblem 2
            subproblem.addConstr(
                2 * x[0] - x[1] + 7 * x[2] + 5 * x[3] + 2 * y[0] + y[1] + 3 * y[2] >= 50
            )
            subproblem.addConstr(
                3 * x[0] - 10 * x[1] + 4 * x[2] + 1 * x[3] + 3 * y[0] - y[1] + y[2] >= 30
            )

        for i in range(len(self.x_values)):
            #Adding constraints for fixing the x-variables to predetermined values
            subproblem.addConstr(
                x[i] == self.x_values[i] , name = f"x_{i}"
            )

        #Declaring the objective function
        objective = 0.5*(y[0] + 2* y[1] + 4* y[2])
        subproblem.setObjective(objective, GRB.MINIMIZE)

        #Solving the model
        subproblem.optimize()

        #Preparing the variables for returning
        y_values = [y[i].X for i in range(3)]
        sensitivities = [subproblem.getConstrByName(f"x_{i}").Pi for i in range(len(self.x_values))]

        return y_values,sensitivities

