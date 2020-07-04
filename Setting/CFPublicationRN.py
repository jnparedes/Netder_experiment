import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Setting.AFPublication import AFPublication
import random
from Ontological.Atom import Atom
from Ontological.Constant import Constant

class CFPublicationRN(AFPublication):

	def __init__(self, node, neighbours, af_post_database, dataset, new_post_prob, share_post_prob):
		super().__init__(node, dataset, af_post_database, new_post_prob)
		self._neighbours = neighbours
		self._share_post_prob = share_post_prob

	def get_new_publication(self):
		result = None
		random_value = random.random()
		if random_value <= 0.1:
			result = self._get_new_publication(True)
		else:
			result = self._get_new_publication(False)

		return result

	def get_publication(self):
		result = super().get_publication()
		if result is None:
			if ((random.random() <= (self._new_post_prob + self._share_post_prob)) and (len(self._neighbours) > 0)):
				#category = self.get_dominant_category_neigh()
				#post_index = None
				#if not category is None:
					#post_index = self._dataset.get_random_pub_index(category)
				post_index = self.get_publication_neigh()
				#index = random.randint(0, len(self._neighbours) - 1)
				#node = self._neighbours[index]
				#post_index = self._af_post_database.get_random_pub_index(node)
				if not post_index is None:
					result = Atom("posted", [Constant(str(self._node.getId())), Constant(str(post_index)), Constant(str(self._time))])

		self._time += 1
		if not result is None:
			self._history_publications.append(result)

		return result

	
	def get_dominant_category_neigh(self):
		result = None
		category_kinds = self._dataset.get_category_kinds()
		counter = [0] * len(category_kinds)
		for neigh in self._neighbours:
			category = self._af_post_database.get_dominant_category(neigh, self._time)
			if not category is None:
				for x in range(len(category_kinds)):
					if category == category_kinds[x]:
						counter[x] += 1
						break

		max_counter = max(counter)
		if max_counter > 0:
			result = category_kinds[counter.index(max_counter)]

		return result

	def get_publication_neigh(self):
		result = None
		category = self.get_dominant_category_neigh()
		if not category is None:
			for neigh in self._neighbours:
				result = self._af_post_database.get_publication(neigh.getId(), category)
				if not result is None:
					break

		return result



