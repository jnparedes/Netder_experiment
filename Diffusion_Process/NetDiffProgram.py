import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Diffusion_Process.NetDiffInterpretation import NetDiffInterpretation

class NetDiffProgram:

	def __init__(self, net_diff_graph, tmax, facts = [], local_rules = [], global_rules = []):
		self._net_diff_graph = net_diff_graph
		self._tmax = tmax
		self._facts = facts
		self._local_rules = local_rules
		self._global_rules = global_rules

	def diffusion(self):
		interp = NetDiffInterpretation(self._net_diff_graph, self._tmax)
		for fact in self._facts:
			interp.applyFact(fact)

		for rule in self._local_rules:
			interp.applyLocalRule(rule)

		for rule in self._global_rules:
			interp.applyGlobalRule(rule)

		return interp