import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Ontological.PredictionsFakeNews import PredictionsFakeNews
from Ontological.Atom import Atom
from Ontological.Constant import Constant
import json

class PredictionsFakeNewsRob(PredictionsFakeNews):

	def __init__(self, name, results_loc = None, fk_threshold = None):
		super().__init__(name, results_loc, fk_threshold)

	def get_atoms(self, id_posts):
		resultado = []
		if len(id_posts) > 0:
			new_id_posts = self.get_id_posts(id_posts, self._fk_threshold)
			for new_id_post in new_id_posts:
				resultado.append(Atom(self._name, [Constant(str(new_id_post))]))

		return resultado

	def get_id_posts(self, id_posts, threshold):
		resultado = []
		if len(id_posts) > 0:
			with open(self._results_loc) as json_file:
					data = json.load(json_file)
					for id_post in id_posts:
						for item in data:
							if (item['id'] == id_post) and (float(item['predictions']['fake_news']) >= threshold):
								resultado.append(id_post)
								break
		return resultado

	def is_greater_than(self, id_post, threshold):
		resultado = False

		return resultado
