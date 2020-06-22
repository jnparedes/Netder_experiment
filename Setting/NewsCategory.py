from Ontological.Atom import Atom
from Ontological.Constant import Constant

class NewsCategory:

	def __init__(self, af_post_database):
		self._af_post_database = af_post_database
		self._time = 0
		self._atoms = []

	def get_atoms(self, time):
		result = []
		if time >= len(self._atoms):
			news = self._af_post_database.get_news()
			dataset = self._af_post_database.get_dataset()


			for id_post in news[self._time]:
				category = dataset.get_category(id_post)
				result.append(Atom('news_category', [Constant(str(id_post)), Constant(str(category))]))
			self._atoms.append(result)
			self._time += 1
		else:
			result = self._atoms[time]	

		return result