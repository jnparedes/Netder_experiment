from Ontological.Atom import Atom

class Distinct(Atom):

	def __init__(self, value1, value2):
		super().__init__('distinct', [value1, value2])

	def is_mapped(self, atom):
		result = False
		result = (self._terms[0].isInstanced() and self._terms[1].isInstanced()) and (self._terms[0].getValue() != self._terms[1].getValue())
		return result

	def get_mapping(self, atom):
		return {}