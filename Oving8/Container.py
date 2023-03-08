class Container:

	def __init__(self, container_id, weight):
		self.container_id = container_id
		self.weight = weight

	@staticmethod
	def sort_array_weight_descending(containers):
		return sorted(containers, key=lambda container: container.weight, reverse=True)

	@staticmethod
	def sort_array_weight_ascending(containers):
		return sorted(containers, key=lambda container: container.weight, reverse=False)
