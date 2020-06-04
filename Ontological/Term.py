class Term:

	def __init__(self, id, value = None):
		self._id = id
		self._value = value

	def getId(self):
		return self._id

	def getValue(self):
		return self._value

	def setValue(self, value):
		self._value = value

	def setId(self, id):
		self._id = id

	def __eq__(self, term):
		result = False
		if term is None:
			result = (self is term)
		else:
			result = (self._id == term.getId())

		return result

	def isInstanced(self):
		return self._value != None

	def can_be_instanced(self):
		return not self.isInstanced()

	def __str__(self):
		return "id: " + str(self._id) + " value: " + str(self._value)