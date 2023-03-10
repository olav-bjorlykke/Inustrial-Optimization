import random
import random as rd
import time


class Solution:

	def __init__(self, n_bays, n_stacks, n_tiers):
		self.n_bays = n_bays
		self.n_stacks = n_stacks
		self.n_tiers = n_tiers

		self.flow_x = [[[0 for _ in range(n_tiers)] for _ in range(n_stacks)] for _ in range(n_bays)]
		self.objective = float("inf")
		self.cog = [0, 0]
		self.total_weight_containers = 0

	def copy(self):
		"""
		Make a copy of the Solution object
		:return: Copy of the object
		"""
		new_solution = Solution(self.n_bays, self.n_stacks, self.n_tiers)

		for bay in range(self.n_bays):
			for stack in range(self.n_stacks):
				for tier in range(self.n_tiers):
					new_solution.flow_x[bay][stack][tier] = self.flow_x[bay][stack][tier]

		new_solution.objective = self.objective
		new_solution.cog = self.cog
		new_solution.total_weight_containers = self.total_weight_containers

		return new_solution

	def construct(self):
		"""
		Simple construction heuristic.
		Takes the first container in the list, and places it in the
		first location. The next is placed in the second location and
		so on.
		"""

		i = 0

		for bay in range(self.n_bays):
			for stack in range(self.n_stacks):
				for tier in range(self.n_tiers):
					self.flow_x[bay][stack][tier] = i
					i += 1

	def calculate_objective(self, containers):
		"""
		Denne metoden regner ut og oppdaterer målfunksjonsverdien til Solution-objektet.
		:param containers: list of Container objects
		"""

		# Her vil vi at cog (centre of gravity) skal ligge
		gravity_goal = [self.n_bays/2.0, self.n_stacks/2.0]


		# Lager en liste som brukes til å regne ut den aktuelle cog-en
		gravity_this = [0.0, 0.0]

		sum_container_weight = 0

		for bay in range(self.n_bays):
			for stack in range(self.n_stacks):

				sum_tier = 0

				for tier in range(self.n_tiers):
					container_weight = containers[self.flow_x[bay][stack][tier]].weight
					sum_tier += container_weight
					sum_container_weight += container_weight

				gravity_this[0] += (bay + 0.5) * sum_tier
				gravity_this[1] += (stack + 0.5) * sum_tier

		gravity_this[0] /= sum_container_weight
		gravity_this[1] /= sum_container_weight

		evaluation = (gravity_goal[0] - gravity_this[0])**2 + (gravity_goal[1] - gravity_this[1])**2

		self.objective = evaluation
		self.cog = gravity_this
		self.total_weight_containers = sum_container_weight

	def print_solution(self, containers):
		print("Current solution:")

		for bay in range(self.n_bays):
			for stack in range(self.n_stacks):
				for tier in range(self.n_tiers):
					print(f"Bay: {bay}, stack: {stack}, tier: {tier}, container: {self.flow_x[bay][stack][tier]} , Weight:{containers[self.flow_x[bay][stack][tier]].weight}" )

	def pretty_print_solution(self, containers):
		tiers = []
		for tier in range(self.n_tiers):
			stacks = []
			for stack in range(self.n_stacks):
				bays = []
				for bay in range(self.n_bays):
					bays.append([self.flow_x[bay][stack][tier], containers[self.flow_x[bay][stack][tier]].weight])
				stacks.append(bays)
			tiers.append(stacks)

		for tier in tiers:
			for stack in tier:
				print(stack)

	def construction_improved(self, containers):
		"""
		Denne metoden implementerer en konstruksjonsheuristikk. Den sorterer containere fra høyest til lavest vekt.
		For deretter å plassere dem ut i at mønster som reverseres på annethvert dekk.

		Heuristikken er svakere dersom det er et odde antall dekk, enn dersom det er et partall.

		:param containers:
		:return:
		"""

		#Sorting the containers based on weight
		container_list = sorted(containers, key = lambda container: container.weight, reverse=True)

		i = 0
		alter = True
		for tier in range(self.n_tiers):
			stack_list = [stack for stack in range(self.n_stacks) for _ in range(self.n_bays)]
			while stack_list:
				if self.n_bays % 2 == 0:
					for bay in reversed(range(0, int(self.n_bays / 2))):
						if alter:
							self.flow_x[bay][stack_list.pop(random.randint(0,len(stack_list)-1))][tier] = container_list[i].container_id
							i += 1
							self.flow_x[self.n_bays - bay - 1][stack_list.pop(random.randint(0,len(stack_list)-1))][tier] = container_list[i].container_id
							i += 1
						else:
							self.flow_x[self.n_bays - bay - 1][stack_list.pop(random.randint(0,len(stack_list)-1))][tier] = container_list[i].container_id
							i += 1
							self.flow_x[bay][stack_list.pop(random.randint(0,len(stack_list)-1))][tier] = container_list[i].container_id
							i += 1
						alter = not alter
				else: #TODO: Add functionality for handling odd number of bays
					pass

	def local_search_two_swap(self, containers):

		start_time = time.time()

		test_ship = self.copy()
		objective = test_ship.objective
		i = 0 
		while True:
			if i % 100 == 0:
				print(i)
			i += 1
			#Array for storing all improved solutions
			solution_array = []

			#iterating through all containers
			for tier in range(test_ship.n_tiers):
				for stack in range(test_ship.n_stacks):
					for bay in range(test_ship.n_bays):

						#Iterating thorugh all other containers that have not yet been tried
						for tier_2 in range(tier,test_ship.n_tiers):
							for stack_2 in range(stack,test_ship.n_stacks):
								for bay_2 in range(bay,test_ship.n_bays):
									#Making a copy of the vessel to test the solution
									test_ship_2 = test_ship.copy()

									#Swapping Two containers
									test_ship_2.flow_x[bay_2][stack_2][tier_2] = test_ship.flow_x[bay][stack][tier]
									test_ship_2.flow_x[bay][stack][tier] = test_ship.flow_x[bay_2][stack_2][tier_2]

									#Calculating objective of the two solutions
									test_ship_2.calculate_objective(containers)

									if test_ship_2.objective < test_ship.objective:
										solution_array.append(test_ship_2.copy())

			if solution_array:
				#Fetching the best from the newly discovered improved solutions and setting that to be the new_best solution:
				new_best = max(solution_array , key=lambda solution: solution.objective)
				test_ship = new_best.copy()
			else:
				break


		#Copying the best solution to this object
		for bay in range(self.n_bays):
			for stack in range(self.n_stacks):
				for tier in range(self.n_tiers):
					self.flow_x[bay][stack][tier] = test_ship.flow_x[bay][stack][tier]

		print("Runtime of Two-Swap:", time.time() - start_time)

	def local_search_three_swap(self, containers):
		test_ship = self.copy()
		objective = test_ship.objective
		i = 0
		while i < 100:
			# Array for storing all improved solutions
			solution_array = []

			# iterating through all containers
			for tier in range(test_ship.n_tiers):
				for stack in range(test_ship.n_stacks):
					for bay in range(test_ship.n_bays):

						# Iterating through all other containers that have not yet been tried
						for tier_2 in range(tier, test_ship.n_tiers):
							for stack_2 in range(stack, test_ship.n_stacks):
								for bay_2 in range(bay, test_ship.n_bays):

									#Iterating through the remaining containers:
									for tier_3 in range(tier_2, test_ship.n_tiers):
										for stack_3 in range(stack_2, test_ship.n_stacks):
											for bay_3 in range(bay_2, test_ship.n_bays):
												test_ship_2 = test_ship.copy()
												test_ship_3 = test_ship.copy()

												# Swapping Three containers: 2 = 1 , 3 = 2 , 1 = 3
												test_ship_2.flow_x[bay_2][stack_2][tier_2] = test_ship.flow_x[bay][stack][tier]
												test_ship_2.flow_x[bay_3][stack_3][tier_3] = test_ship.flow_x[bay_2][stack_2][tier_2]
												test_ship_2.flow_x[bay][stack][tier] = test_ship.flow_x[bay_3][stack_3][tier_3]

												# Swapping Three containers: 2 = 3 , 3 = 1 , 1 = 2
												test_ship_3.flow_x[bay_2][stack_2][tier_2] = test_ship.flow_x[bay_3][stack_3][tier_3]
												test_ship_3.flow_x[bay_3][stack_3][tier_3] = test_ship.flow_x[bay][stack][tier]
												test_ship_3.flow_x[bay][stack][tier] = test_ship.flow_x[bay_2][stack_2][tier_2]


												# Calculating objective of the two solutions
												test_ship_2.calculate_objective(containers)
												test_ship_3.calculate_objective(containers)

												if test_ship_2.objective < test_ship.objective:
													solution_array.append(test_ship_2.copy())

												if test_ship_3.objective < test_ship.objective:
													solution_array.append(test_ship_3.copy())


			if solution_array:
				#Fetching the best from the newly discovered improved solutions and setting that to be the new_best solution:
				new_best = max(solution_array , key=lambda solution: solution.objective)
				test_ship = new_best.copy()
			else:
				break
			i += 1

		#Copying the best solution to this object
		for bay in range(self.n_bays):
			for stack in range(self.n_stacks):
				for tier in range(self.n_tiers):
					self.flow_x[bay][stack][tier] = test_ship.flow_x[bay][stack][tier]

	def tabu_search_heuristic(self, containers, n_iterations):
		start_time = time.time()
		test_ship = self.copy()
		objective = test_ship.objective
		i = 0
		tabu_swaps = []
		while True:
			if i % 100 == 0:
				print(i)

			i += 1
			# Array for storing all improved solutions
			solution_array = []

			# iterating through all containers
			for tier in range(test_ship.n_tiers):
				for stack in range(test_ship.n_stacks):
					for bay in range(test_ship.n_bays):

						# Iterating thorugh all other containers that have not yet been tried
						for tier_2 in range(tier, test_ship.n_tiers):
							for stack_2 in range(stack, test_ship.n_stacks):
								for bay_2 in range(bay, test_ship.n_bays):
									if [[bay, stack, tier], [bay_2, stack_2, tier_2]] in tabu_swaps:
										tabu_swaps.pop(0)


									else:
										# Making a copy of the vessel to test the solution
										test_ship_2 = test_ship.copy()

										# Swapping Two containers
										test_ship_2.flow_x[bay_2][stack_2][tier_2] = test_ship.flow_x[bay][stack][tier]
										test_ship_2.flow_x[bay][stack][tier] = test_ship.flow_x[bay_2][stack_2][tier_2]

										# Calculating objective of the two solutions
										test_ship_2.calculate_objective(containers)

										if test_ship_2.objective < test_ship.objective:
											solution_array.append(
												[test_ship_2.copy(), [bay, stack, tier], [bay_2, stack_2, tier_2]])


			if solution_array:
				# Fetching the best from the newly discovered improved solutions and setting that to be the new_best solution:
				new_best = max(solution_array, key=lambda solution: solution[0].objective)
				tabu_swaps.append([new_best[1],new_best[2]])
				test_ship = new_best[0].copy()
			else:
				break


			# Copying the best solution to this object
		for bay in range(self.n_bays):
			for stack in range(self.n_stacks):
				for tier in range(self.n_tiers):
					self.flow_x[bay][stack][tier] = test_ship.flow_x[bay][stack][tier]

		print("Runtime of Tabu Search:", time.time() - start_time)


