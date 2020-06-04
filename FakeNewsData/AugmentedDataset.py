from FakeNewsData.Dataset import Dataset
import random

class AugmentedDataset(Dataset):

	def __init__(self, location, limit_item = 5000):
		super().__init__(location, limit_item)
		self._category_kinds = ["A", "B", "C", "D", "E"]
		self._categories = {}
		dominant_prob = 0.7
		self._prob_categories = {}
		aux_prob = {}
		for index in range(len(self._category_kinds)):
			if index == 0:
				aux_prob[self._category_kinds[index]] = dominant_prob
			else:
				aux_prob[self._category_kinds[index]] = (1 - dominant_prob) / (len(self._category_kinds) - 1)
		self._prob_categories[True] = aux_prob

		aux_prob = {}
		for category in self._category_kinds:
			aux_prob[category] = 1 / len(self._category_kinds)

		self._prob_categories[False] = aux_prob

		

	def _init_categories(self):
		if len(self._categories) == 0:
			gt = self.get_ground_truth()
			for key in gt.keys():
				random_value = random.random()
				prob_dict = self._prob_categories[gt[key]]
				prob_acum = 0
				for category in prob_dict.keys():
					prob_acum = prob_acum + prob_dict[category]
					if random_value <= prob_acum:
						self._categories[key] = category
						break

	def get_category_kinds(self):
		return self._category_kinds

	def get_category(self, id_post):
		result = None
		self._init_categories()
		if len(self._categories) > 0:
			result = self._categories[id_post]
		return result

	def get_prob_categories(self):
		return self._prob_categories

'''
	def get_random_pub_index(self, category):
		self._init_categories()
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

		return x'''

