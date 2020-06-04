import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Ontological.NetDERRule import NetDERRule

class NetDERTGD(NetDERRule):

	def __init__(self, rule_id, ont_body = [], net_body = [], ont_head = [], net_head = [], global_cond = []):
		super().__init__(rule_id, ont_body, net_body, global_cond)
		self._ont_head = ont_head
		self._net_head = net_head

	def get_ont_head(self):
		return self._ont_head

	def get_net_head(self):
		return self._net_head