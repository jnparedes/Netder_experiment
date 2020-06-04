from Ontological.Atom import Atom
from Ontological.Constant import Constant

class NewsCategory:

	def __init__(self, af_post_database):
		self._af_post_database = af_post_database
		self._time = 0

	def get_atoms(self):
		result = []
		news = self._af_post_database.get_news()
		dataset = self._af_post_database.get_dataset()


		for id_post in news[self._time]:
			category = dataset.get_category(id_post)
			result.append(Atom('news_category', [Constant(str(id_post)), Constant(str(category))]))
		self._time += 1	

		return result