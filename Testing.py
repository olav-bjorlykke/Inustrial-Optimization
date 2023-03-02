
import gurobipy as gp
from gurobipy import GRB


#Settin up sets
Nurses = [f"{i}" for i in range(1,10)]
Shifts = ["Shift1", "Shift2", "Shift3"]
Days = [f"{i}" for i in range(1,10)]

rNurses = [i for i in range(len(Nurses))]
rShifts = [i for i in range(len(Shifts))]
rDays = [i for i in range(len(Days))]

#Setting up parameters


#Setting up a dict with shift requirements
#TODO: Set the shift requirements to be correct
shiftStaffingRequirements = {
    "1": {"Shift1": 2, "Shift2": 2, "Shift3": 2},
    "2": {"Shift1": 2, "Shift2": 2, "Shift3": 2},
    "3": {"Shift1": 3, "Shift2": 2, "Shift3": 2},
    "4": {"Shift1": 3, "Shift2": 2, "Shift3": 2},
    "5": {"Shift1": 3, "Shift2": 2, "Shift3": 2},
    "6": {"Shift1": 3, "Shift2": 2, "Shift3": 2},
    "7": {"Shift1": 3, "Shift2": 2, "Shift3": 2},
    "8": {"Shift1": 2, "Shift2": 2, "Shift3": 2},
    "9": {"Shift1": 2, "Shift2": 2, "Shift3": 2},
}

#Parameter for cost of staffing a shift
#TODO: Add correct costs
shiftCost = {
    "1": {"Shift1": 1200, "Shift2": 1200+200, "Shift3": 1500+200},
    "2": {"Shift1": 1200, "Shift2": 1200+200, "Shift3": 1500+200},
    "3": {"Shift1": 1000, "Shift2": 1200, "Shift3": 1500},
    "4": {"Shift1": 1000, "Shift2": 1200, "Shift3": 1500},
    "5": {"Shift1": 1000, "Shift2": 1200, "Shift3": 1500},
    "6": {"Shift1": 1000, "Shift2": 1200, "Shift3": 1500},
    "7": {"Shift1": 1000, "Shift2": 1200, "Shift3": 1500},
    "8": {"Shift1": 1200, "Shift2": 1200+200, "Shift3": 1500+200},
    "9": {"Shift1": 1200, "Shift2": 1200+200, "Shift3": 1500+200},
}

#Paramater for cost of shift for a substitute nurse
#TODO: Add correct costs
shiftCostSubstitute = {
    "1": {"Shift1": 2000, "Shift2": 2400, "Shift3": 3000},
    "2": {"Shift1": 2000, "Shift2": 2400, "Shift3": 3000},
    "3": {"Shift1": 2000, "Shift2": 2400, "Shift3": 3000},
    "4": {"Shift1": 2000, "Shift2": 2400, "Shift3": 3000},
    "5": {"Shift1": 2000, "Shift2": 2400, "Shift3": 3000},
    "6": {"Shift1": 2000, "Shift2": 2400, "Shift3": 3000},
    "7": {"Shift1": 2000, "Shift2": 2400, "Shift3": 3000},
    "8": {"Shift1": 2000, "Shift2": 2400, "Shift3": 3000},
    "9": {"Shift1": 2000, "Shift2": 2400, "Shift3": 3000},
}

#Setting constant Params
shiftLength = 8
L = len(Days)/7



#Create the model
m = gp.Model("Nurse Rostering")
m.ModelSense = GRB.MINIMIZE

#Add variables
x = m.addVars(rNurses, rShifts, rDays, vtype="B", name="x")
y = m.addVars(rShifts, rDays, vtype="B", name="y")

#Max one shift per day constraint:
for n in rNurses:
    for d in rShifts:
        m.addConstr(gp.quicksum(x[n,s,d] for s in rShifts) <= 1)

#Atleast 11 hours of rest constraint:
for d in rDays[1:]:
    for n in rNurses:
        m.addConstr(x[n,0,d] + x[n,1,d-1] +x[n,2,d-1] <= 1)
        m.addConstr(x[n, 1, d - 1] + x[n, 0, d] + x[n, 2, d - 1]  <= 1)


#Each shift has enough Personnel
for d in rDays:
    for s in rShifts:
        print("Day",d, "Shift", d, "req:", shiftStaffingRequirements[Days[d]][Shifts[s]])
        m.addConstr(gp.quicksum(x[n, s, d] for n in rNurses) + y[s, d] >= shiftStaffingRequirements[Days[d]][Shifts[s]])

#Create the objective function:
#TODO: Add penalties and hours constraints
m.setObjective(
    gp.quicksum(x[n,s,d] * shiftCost[Days[d]][Shifts[s]] for n in rNurses for s in rShifts for d in rDays) +
    gp.quicksum(y[s,d] * shiftCostSubstitute[Days[d]][Shifts[s]] for s in rShifts for d in rDays)
)


m.optimize()
