from abc import ABC

class NetDERRule(ABC):

	def __init__(self, rule_id, ont_body=[], net_body=[], global_cond=[]):
		self._id = rule_id
		self._ont_body = ont_body
		self._net_body = net_body
		self._global_cond = global_cond

	def get_id(self):
		return self._id

	def get_ont_body(self):
		return self._ont_body

	def get_net_body(self):
		return self._net_body

	def get_global_cond(self):
		return self._global_cond