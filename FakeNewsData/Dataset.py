from abc import ABC,abstractmethod

class Dataset(ABC):

	def __init__(self, location, limit_item = 5000):
		self._location = location
		self._limit_item = limit_item

	@abstractmethod
	def _load_data(self):
		pass

	def get_data(self):
		return self._load_data()

	@abstractmethod
	def get_ground_truth(self):
		pass
	
