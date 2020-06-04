from abc import ABC, abstractmethod
import random

class AFPost(ABC):

	def __init__(self, id, af_publication):
		self._id = id
		self._new_post_prob = 0
		self._share_post_prob = 0
		self._nothing_do_prob = 0
		self._af_publication = af_publication
		self._dataset = dataset

	@abstractmethod
	def get_post(self):
		result = None
		if random.random() <= self._new_post_prob:
			result = self._af_publication.get_publication()

		return result

		