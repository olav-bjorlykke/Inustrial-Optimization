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
		print("grav goal",gravity_goal)

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
		container_list = sorted(containers, key = lambda container: container.weight)

		i = 0
		for bay in range(self.n_bays):
			for stack in range(self.n_stacks):
				for tier in range(self.n_tiers):
					self.flow_x[bay][stack][tier] = container_list[i].container_id
					i += 1






	def local_search_two_swap(self, containers):
		print("Oppgave 2a")

	def local_search_three_swap(self, containers):
		print("Oppgave 2b")

	def tabu_search_heuristic(self, containers, n_iterations):
		print("Oppgave 3")
