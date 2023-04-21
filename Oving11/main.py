from sub_problem import SubProblem
from master_problem import MasterProblem

y_values_sub1 = []
y_values_sub2 = []
sensitivities_sub1 = []
sensitivities_sub2 = []
prev_x_values = []
solutions = []

for i in range(10):
    print(f"*********************************         {i}           *********************************")
    master = MasterProblem(y_values_sub1,y_values_sub2,sensitivities_sub1,sensitivities_sub2,prev_x_values)
    x_i, solution = master.solve()
    sub1 = SubProblem(x_i, 1)
    sub2 = SubProblem(x_i, 1)
    y_1, sens1 = sub1.solve()
    y_2, sens2 = sub2.solve()

    y_values_sub1.append(y_1)
    y_values_sub2.append(y_2)
    sensitivities_sub1.append(sens2)
    sensitivities_sub2.append(sens1)
    prev_x_values.append(x_i)

    solutions.append([i, solution])

print(solutions)



