from Setting.NewPublicationFactory import NewPublicationFactory
from Ontological.Atom import Atom
from Ontological.Constant import Constant
import random

class SocialBotnet:

	def __init__(self, dataset = None, fn_prob = 1, new_post_prob = 1):
		self._members = []
		self._posts = []
		self._new_pub_factory = NewPublicationFactory(dataset)
		self._fn_prob = fn_prob
		self._new_post_prob = new_post_prob

	def set_dataset(self, dataset):
		self._new_pub_factory.set_dataset(dataset)

	def set_fn_prob(self, fn_prob):
		self._fn_prob = fn_prob

	def get_fn_prob(self):
		return self._fn_prob

	def get_new_post_prob(self):
		return self._new_post_prob

	def set_new_post_prob(self, new_post_prob):
		self._new_post_prob = new_post_prob

	def add_member(self, node):
		if not (node in self._members):
			self._members.append(node)

	def get_new_publication(self, node, label, time):
		result = None
		index = None
		if node in self._members:
			index = self._new_pub_factory.get_index_new_publ(label)

			self._posts.append(index)

			result = Atom("posted", [Constant(str(node)), Constant(str(index)), Constant(str(time))])

		return result

	def get_publication(self, node, time):
		result = None
		if node in self._members:
			if time < len(self._posts):
				index = self._posts[time]
				if not index is None:
					result = Atom("posted", [Constant(str(node)), Constant(str(index)), Constant(str(time))])
			else:
				rand_num = random.uniform(0,1)
				if rand_num <= self._new_post_prob:
					label = False
					rand_num = random.uniform(0,1)
					if rand_num <= self._fn_prob:
						label = True

					result = self.get_new_publication(node, label, time)
				else:
					self._posts.append(None)

		return result

	def get_members(self):
		return self._members

	def set_categories_order(self, categories_order):
		self._new_pub_factory.set_categories_order(categories_order)

	def set_prob_categories(self, prob_categories):
		self._new_pub_factory.set_prob_categories(prob_categories)

	def get_posts(self):
		return self._posts
