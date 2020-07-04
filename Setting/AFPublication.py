import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from abc import ABC, abstractmethod
import random
import copy
from Ontological.Atom import Atom
from Ontological.Constant import Constant
from Setting.NewPublicationFactory import NewPublicationFactory

class AFPublication(ABC):

	def __init__(self, node, dataset, af_post_database = None, new_post_prob = 1):
		self._dataset = dataset
		self._node = node
		self._time = 0
		self._new_post_prob = new_post_prob
		self._history_publications = []
		self._af_post_database = af_post_database
		self._categories_order = copy.deepcopy(dataset.get_category_kinds())
		random.shuffle(self._categories_order)
		'''
		aux_categories_order = copy.deepcopy(self._dataset.get_category_kinds())[1:]
		random.shuffle(aux_categories_order)
		dc_probabilities = [0.6, 0.2, 0.2]
		position = None
		random_value = random.random()
		p = 0
		for index in range(len(dc_probabilities)):
			p = p + dc_probabilities[index]
			if random_value <= p:
				position = index
				break

		self._categories_order = aux_categories_order[:position] + [self._dataset.get_category_kinds()[0]] + aux_categories_order[position:]'''
		self._prob_categories = {True: [0.4, 0.2, 0.2, 0.1, 0.1], False: [0.4, 0.2, 0.2, 0.1, 0.1]}
		#self._prob_categories = [0.2, 0.2, 0.2, 0.2, 0.2]
		self._new_pub_factory = NewPublicationFactory(self._dataset, self._categories_order, self._prob_categories)
	
	def _get_new_publication(self, label = None):
		result = None

		index = self._new_pub_factory.get_index_new_publ(label)
		result = Atom("posted", [Constant(str(self._node.getId())), Constant(str(index)), Constant(str(self._time))])
		
		return result

	@abstractmethod
	def get_new_publication(self):
		pass	
	
	def get_publication(self):
		result = None
		if random.random() <= self._new_post_prob:
			result = self.get_new_publication()

		return result

	def get_node(self):
		return self._node

	def get_random_pub_index(self):
		result = None
		if len(self._history_publications) > 0:
			index = random.randint(0, len(self._history_publications) - 1)
			result = self._history_publications[index].get_terms()[1].getId()
		
		return result

	def get_dominant_category(self, time):
		result = None
		category_kinds = self._dataset.get_category_kinds()
		counter = [0] * len(category_kinds)
		for t in range(time + 1):
			if t < len(self._history_publications):
				post = self._history_publications[t]
			#for post in self._history_publications:
				for x in range(len(category_kinds)):
					if self._dataset.get_category(post.get_terms()[1].getId()) == category_kinds[x]:
						counter[x] += 1
						break
			else:
				break	
		max_counter = max(counter)
		if max_counter > 0:
			result = category_kinds[counter.index(max_counter)]
		
		return result

	#def get_history_publications(self):
	#	return self._history_publications