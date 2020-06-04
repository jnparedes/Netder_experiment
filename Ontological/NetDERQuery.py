import copy

class NetDERQuery:

	def __init__(self, exist_var = [], ont_cond = [], net_cond = [], global_cond = [], time = []):
		self._exist_var = []
		self._ont_cond = ont_cond
		for var in exist_var:
			for atom in self._ont_cond:
				if var in atom.get_terms():
					self._exist_var.append(var)
					break

		self._net_cond = net_cond
		self._global_cond = global_cond
		self._time = time

	def get_exist_var(self):
		return self._exist_var

	def get_ont_body(self):
		return self._ont_cond

	def get_net_body(self):
		return self._net_cond

	def get_global_cond(self):
		return self._global_cond

	def get_time(self):
		return self._time

	def get_disjoint_queries(self):
		result = []
		disjoint_atoms = []
		for atom in self._ont_cond:
			found_atom = False
			for term in atom.get_terms():
				found_position = False
				index = 0
				last_used_index = 0
				cloned_disjoint_atoms = copy.deepcopy(disjoint_atoms)
				for item in cloned_disjoint_atoms:
					for other_atom in item:
						if not other_atom == atom:
							if term in other_atom.get_terms():
								if not found_position:
									if not atom in disjoint_atoms[index]:
										last_used_index = index
										disjoint_atoms[last_used_index].append(copy.deepcopy(atom))
										found_position = True
										found_atom = found_atom or found_position
										break
							
								elif last_used_index != index:
									if not other_atom in disjoint_atoms[last_used_index]:
										disjoint_atoms[last_used_index].append(copy.deepcopy(other_atom))
					
									disjoint_atoms[index].remove(other_atom)
									if len(disjoint_atoms[index]) == 0:
										disjoint_atoms.remove(disjoint_atoms[index])
						
					index += 1
					

			if not found_atom:
				terms = copy.deepcopy(atom.get_terms())
				last_used_index = len(disjoint_atoms)
				disjoint_atoms.append([copy.deepcopy(atom)])

		for item in disjoint_atoms:
			result.append(NetDERQuery(exist_var = self._exist_var, ont_cond = item, time = self._time))

		return result
