from abc import ABC, abstractmethod
class PredictionsFakeNews(ABC):

	def __init__(self, name, results_loc, fk_threshold):
		self._results_loc = results_loc
		self._fk_threshold = fk_threshold
		self._name = name

	@abstractmethod
	def get_atoms(self, id_posts):
		pass

	def set_results_loc(self, results_loc):
		self._results_loc = results_loc

	def set_fk_threshold(self, fk_threshold):
		self._fk_threshold = fk_threshold