from FakeNewsData.DatasetCSVLiar import DatasetCSVLiar
import random

class AugmentedDatasetCSVLiar(DatasetCSVLiar):

	def __init__(self):
		super().__init__()
		self._category_kinds = ["A", "B", "C", "D", "E"]
		self._categories = []
		for index in range(len(self.get_data())):
			self._categories.append(random.choice(self._category_kinds))

	def get_category_kinds(self):
		return self._category_kinds

	def get_category(self, id_post):
		return self._categories[id_post]

	def get_random_pub_index(self, category):
		start = random.randint(0, len(self._categories))
		found = False
		x = None
		for index in range(start, len(self._categories)):
			if self._categories[index] == category:
				x = index
				found = True
				break

		if not found:
			for index in range(start):
				if self._categories[index] == category:
					x = index
					break

		return x
