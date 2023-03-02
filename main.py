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




#Adding Constraints:

#Max one shift per day constraint:
for n in rNurses:
    for d in rDays:
        m.addConstr(gp.quicksum(x[n,s,d] for s in rShifts) <= 1)


#Atleast 11 hours of rest constraint:
for d in rDays[1:]:
    for n in rNurses:
        m.addConstr(x[n,0,d] + x[n,1,d-1] +x[n,2,d-1] <= 1)
        m.addConstr(x[n, 1, d - 1] + x[n, 0, d] + x[n, 2, d - 1]  <= 1)

#Both Days or none of the days in a weekend off
for n in rNurses:
    m.addConstr(gp.quicksum(x[n,s,0]for s in rShifts) == gp.quicksum(x[n,s,1]for s in rShifts))
    m.addConstr(gp.quicksum(x[n, s, 7] for s in rShifts) == gp.quicksum(x[n, s, 8] for s in rShifts))

#Every other weekend off
for n in rNurses:
    m.addConstr(gp.quicksum(x[n,s,0] + x[n,s,7] for s in rShifts) <= 1)

#Work atmost 6 consecutive days:
for n in rNurses:
    for d_num in range(len(rDays[5:9])):
        m.addConstr(gp.quicksum(x[n,s,d] for s in rShifts for d in rDays[d_num:d_num + 5]) <= 6)
    #TODO: Doublecheck that this is the correct iteration for d

#Work atmost 4 consecutive Night shifts:
for n in rNurses:
    for d_num in range(len(Days)-3):
        m.addConstr(gp.quicksum(x[n,s,d] for s in rShifts for d in rDays[d_num:d_num + 3]) <= 4)
    # TODO: Doublecheck that this is the correct iteration for d


#Each shift has enough Personnel
for d in rDays:
    for s in rShifts:
        print("Day",d, "Shift", d, "req:", shiftStaffingRequirements[Days[d]][Shifts[s]])
        m.addConstr(gp.quicksum(x[n, s, d] for n in rNurses) + y[s, d] >= shiftStaffingRequirements[Days[d]][Shifts[s]])

#TODO: Add symmetry breaking constraints

#Create the objective function:
#TODO: Add penalties and hours constraints
m.setObjective(
    gp.quicksum(x[n,s,d] * shiftCost[Days[d]][Shifts[s]] for n in rNurses for s in rShifts for d in rDays) +
    gp.quicksum(y[s,d] * shiftCostSubstitute[Days[d]][Shifts[s]] for s in rShifts for d in rDays)
)


m.optimize()

print('SOLUTION:')

for d in rDays:
    print(f"Day {d}")
    for s in rShifts:
        print(f"Shift{s + 1}:")
        if y[s, d].X > 0:
            print(f"    Substitute")
        for n in rNurses:
            if x[n,s,d].X > 0:
                print(f"    Nurse {n + 1}")









