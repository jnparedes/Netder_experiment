from AFPublication import AFPublication
from SocialBotnet import SocialBotnet
import random
import copy

class CFPublicationFN(AFPublication):

	def __init__(self, node, dataset, af_post_database, fn_prob, new_post_prob = 1, social_botnet = SocialBotnet()):
		super().__init__(node = node, dataset = dataset, af_post_database = af_post_database, new_post_prob = new_post_prob)
		self._social_botnet = social_botnet
		self._social_botnet.add_member(self._node.getId())
		self._social_botnet.set_dataset(dataset)
		self._social_botnet.set_fn_prob(fn_prob)
		self._social_botnet.set_new_post_prob(new_post_prob)

		aux_categories_order = copy.deepcopy(self._dataset.get_category_kinds())[1:]
		self._categories_order = copy.deepcopy(self._dataset.get_category_kinds())[:1]
		random.shuffle(aux_categories_order)
		self._categories_order = self._categories_order + aux_categories_order
		
		self._prob_categories[False] = [0.2, 0.2, 0.2, 0.2, 0.2]
		self._social_botnet.set_categories_order(self._categories_order)
		self._social_botnet.set_prob_categories(self._prob_categories)

	def get_new_publication(self):
		result = None
		result = self._social_botnet.get_new_publication(self._node.getId(), self._time)
		return result

	def get_publication(self):
		result = self._social_botnet.get_publication(self._node.getId(), self._time)
		self._time += 1
		if not result is None:
			self._history_publications.append(result)

		return result

	def set_social_botnet(self, social_botnet):
		self._social_botnet = social_botnet
		self._social_botnet.add_member(self._node.getId())