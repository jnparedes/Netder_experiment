from Ontological.NetDERRule import NetDERRule

class NetDEREGD(NetDERRule):

	def __init__(self, rule_id, ont_body = [], net_body = [], head = [], global_cond = []):
		super().__init__(rule_id, ont_body, net_body, global_cond)
		self._head = head

	def get_head(self):
		return self._head