import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Ontological.Atom import Atom
from Ontological.Constant import Constant

class EarlyPoster:

	def __init__(self, af_post_database):
		self._af_post_database = af_post_database
		self._time = 0
		self._atoms = []

	def get_atoms(self, time):
		result = []
		if time >= len(self._atoms):
			hist_publications = self._af_post_database.get_hist_publications()

			for key in hist_publications[self._time].keys():
				found = False
				post_id = hist_publications[self._time][key]
				for time in range(self._time):
					for other_key in hist_publications[time].keys():
						if hist_publications[time][other_key] == post_id:
							found = True
							break
							break
				if not found:
					result.append(Atom('earlyPoster', [Constant(str(key)), Constant(str(post_id))]))
			self._time += 1
			self._atoms.append(result)
		else:
			result = self._atoms[time]
		
		return result


