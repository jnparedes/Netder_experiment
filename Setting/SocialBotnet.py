from NewPublicationFactory import NewPublicationFactory
from Ontological.Atom import Atom
from Ontological.Constant import Constant
import random

class SocialBotnet:

	def __init__(self, dataset = None, fn_prob = 1):
		self._members = []
		self._posts = []
		self._new_pub_factory = NewPublicationFactory(dataset)
		self._fn_prob = fn_prob

	def set_dataset(self, dataset):
		self._new_pub_factory.set_dataset(dataset)

	def set_fn_prob(self, fn_prob):
		self._fn_prob = fn_prob

	def add_member(self, node):
		if not (node in self._members):
			self._members.append(node)

	def get_new_publication(self, node, time):
		result = None
		index = None
		if node in self._members:
			if time < len(self._posts):
				index = self._posts[time]
			else:
				if random.random() <= self._fn_prob:
					index = self._new_pub_factory.get_index_new_publ(True)
				else:
					index = self._new_pub_factory.get_index_new_publ(False)

				self._posts.append(index)


		result = Atom("posted", [Constant(str(node)), Constant(str(index)), Constant(str(time))])

		return result

	def get_members(self):
		return self._members

	def set_categories_order(self, categories_order):
		self._new_pub_factory.set_categories_order(categories_order)

	def set_prob_categories(self, prob_categories):
		self._new_pub_factory.set_prob_categories(prob_categories)
