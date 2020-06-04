from Ontological.Atom import Atom
from Ontological.Constant import Constant

class Closer:

	def __init__(self, af_post_database):
		self._af_post_database = af_post_database
		self._time = 0
		self._hist = []

	def get_atoms(self):
		result = []
		hist_publications = self._af_post_database.get_hist_publications()
		key_list = list(hist_publications[self._time].keys())
		for user_index in range(len(key_list)):
			user_key = key_list[user_index]
			if user_index + 1 < len(key_list):
				for other_user_index in range(user_index + 1, len(key_list)):
					other_user_key = key_list[other_user_index]
					pair = '(' + str(user_key) + ',' + str(other_user_key) + ')'
					simetric_pair = '(' + str(other_user_key) + ',' + str(user_key) + ')'
					condition = (not simetric_pair in self._hist) and (not pair in self._hist)
					if user_key == other_user_key:
						print('PASA ALGO RAROOOOOOOO')
					if hist_publications[self._time][user_key] == hist_publications[self._time][other_user_key] and condition:
						if Atom('closer', [Constant(other_user_key), Constant(user_key)]) in result:
							print('nooooooooooooooooooo')
						result.append(Atom('closer', [Constant(user_key), Constant(other_user_key)]))
						self._hist.append(pair)

		self._time += 1

		return result