import random
class NewPublicationFactory:

	def __init__(self, dataset = None, categories_order = None, prob_categories = None):
		self._dataset = dataset
		self._categories_order = categories_order
		self._prob_categories = prob_categories

	def set_dataset(self, dataset):
		self._dataset = dataset

	def get_index_new_publ(self, label):
		key = None
		gt = self._dataset.get_ground_truth()
		gt_keys = list(gt.keys())
		index_key = random.randint(0, len(gt_keys) - 1)
		key = gt_keys[index_key]

		acum_prob = 0
		category = None
		random_value = random.random()

		if (not label is None):
			probabilities = self._prob_categories[label]
			for index in range(len(probabilities)):
				acum_prob += probabilities[index]
				if random_value <= acum_prob:
					category = self._categories_order[index]
					break
			while (not gt[key] == label) or (not self._dataset.get_category(key) == category):
				index_key = random.randint(0, len(gt_keys) - 1)
				key = gt_keys[index_key]
		'''else:
			while (not self._dataset.get_category(key) == category):
				index_key = random.randint(0, len(gt_keys) - 1)
				key = gt_keys[index_key]'''
		
		return key

	def set_categories_order(self, categories_order):
		self._categories_order = categories_order

	def set_prob_categories(self, prob_categories):
		self._prob_categories = prob_categories
