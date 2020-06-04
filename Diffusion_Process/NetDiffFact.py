import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Ontological.NetCompTarget import NetCompTarget

class NetDiffFact(NetCompTarget):
	
	def __init__(self, component, label, interval, t_lower, t_upper):
		super().__init__(component, label, interval)
		self._t_upper = t_upper
		self._t_lower = t_lower

	def getTimeUpper(self):
		return self._t_upper

	def getTimeLower(self):
		return self._t_lower

	def __str__(self):
		return str(self._component) + '\n' + str(self._label) + '\n' + str(self._interval) + '\n' + '[' + str(self._t_lower) + ',' + str(self._t_upper) + ']'