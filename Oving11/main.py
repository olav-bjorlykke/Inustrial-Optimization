from sub_problem import SubProblem
from master_problem import MasterProblem

y_values_sub1 = []
y_values_sub2 = []
sensitivities_sub1 = []
sensitivities_sub2 = []
prev_x_values = []
solutions = []
sub1_solutions = []
sub2_solutions = []

for i in range(5):
    print(f"*********************************         {i}           *********************************")
    master = MasterProblem(y_values_sub1,y_values_sub2,sensitivities_sub1,sensitivities_sub2,prev_x_values)
    x_i, solution = master.solve()
    sub1 = SubProblem(x_i, 1)
    sub2 = SubProblem(x_i, 1)
    y_1, sens1, y_1_sol = sub1.solve()
    y_2, sens2, y_2_sol = sub2.solve()

    y_values_sub1.append(y_1)
    y_values_sub2.append(y_2)
    sensitivities_sub1.append(sens2)
    sensitivities_sub2.append(sens1)
    prev_x_values.append(x_i)

    solutions.append([i, solution])
    sub1_solutions.append([i, y_1_sol])
    sub2_solutions.append([i, y_2_sol])


print("master solutions", solutions)
print("sub1 solution", solutions)
print("sub2 solution", solutions)


