import copy
from Ontological.Atom import Atom
from Ontological.Constant import Constant

class PreMember:

	def __init__(self, earlyPoster):
		self._time = 0
		self._atoms = []
		self._earlyPoster = earlyPoster

	def get_atoms(self, time):
		result = []
		if time >= len(self._atoms):
			eps = self._earlyPoster.get_atoms(time)
			for atom in eps:
				for t in range(time + 1):
					clone_eps = copy.deepcopy(self._earlyPoster.get_atoms(t))
					for otherAtom in clone_eps:
						v1 = otherAtom.get_terms()[0].getValue()
						v2 = atom.get_terms()[0].getValue()
						v3 = otherAtom.get_terms()[1].getValue()
						v4 = atom.get_terms()[1].getValue()
						if v1 != v2 and  v3 == v4:
							result.append(Atom('pre_member', [Constant(v1), Constant(v2), Constant(v3)]))
			self._time += 1
			self._atoms.append(result)
		else:
			result = self._atoms[time]

		return result