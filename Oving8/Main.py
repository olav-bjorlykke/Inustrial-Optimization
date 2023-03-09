from Container import Container
from Solution import Solution
from Vessel import Vessel
import random


if __name__ == '__main__':
	# Set data file
	filename = "instance1.txt"

	# Read from data file
	with open(filename, "r") as datafile:
		data = datafile.readlines()

		vessel_dimensions = list(map(int, data[:3]))

		weights = list(map(int, data[3:]))

	containers = []

	# dette er det samme som Vessel(vessel_dimensions[0], vessel_dimensions[1], vessel_dimensions[2])
	vessel = Vessel(*vessel_dimensions)

	for container_id in range(len(weights)):
		containers.append(Container(container_id, weights[container_id]))

	# containers is an array of Container objects
	# vessel is a Vessel object


	# Create a Solution object for the initial solution
	initial_solution = Solution(vessel.n_bays, vessel.n_stacks, vessel.n_tiers)

	# Construct an initial solution
	initial_solution.construct()
	print("Original Heuristic")

	# Evaluate the initial solution
	initial_solution.calculate_objective(containers)
	print("Solution:", initial_solution.objective, "COG", initial_solution.cog[0], initial_solution.cog[1])



	# OPPGAVE 1
	#initial_solution.construction_improved(containers)
	#initial_solution.calculate_objective(containers)
	#print("Improved", initial_solution.objective, "COG", initial_solution.cog[0], initial_solution.cog[1])
	#initial_solution.pretty_print_solution(containers)

	# Implementer denne i Solution.py

	# Sortere containere etter vekt slik:
	# containers_descending = Container.sort_array_weight_descending(containers)
	# containers_ascending = Container.sort_array_weight_ascending(containers)
	###########################################################################

	# Print the initial solution to command window
	#initial_solution.print_solution()


	# Improvement phase

	# Create 3 copies of the initial solution
	new_solution2A = initial_solution.copy()
	new_solution2B = initial_solution.copy()
	new_solution3 = initial_solution.copy()

	# OPPGAVE 2A
	new_solution2A.local_search_two_swap(containers)
	new_solution2A.calculate_objective(containers)
	# Implementer denne i Solution.py
	print("Solution 2A:", new_solution2A.objective, "COG", new_solution2A.cog[0], new_solution2A.cog[1])

	# OPPGAVE 2B
	new_solution2B.local_search_three_swap(containers)
	new_solution2B.calculate_objective(containers)
	# Implementer denne i Solution.py
	print("Solution 2B", new_solution2B.objective, "COG", new_solution2B.cog[0], new_solution2B.cog[1])

	# OPPGAVE 3
	n_iterations = 100
	new_solution2A.tabu_search_heuristic(containers, n_iterations)
	# Implementer denne i Solution.py
	print(new_solution3.objective)
