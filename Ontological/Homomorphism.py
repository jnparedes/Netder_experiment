import copy
class Homomorphism:

	def get_atom_mapping(self, atom, data_base):
		result = []
		for data in data_base:
			if atom.is_mapped(data):
				result.append(atom.get_mapping(data))
		if len(result) == 0:
			result = None
		
		return result

	def get_atoms_mapping(self, atoms, data_base):
		aux_result = [[]]
		aux_mapped_atoms = [copy.deepcopy(atoms)]

		for index in range(0, len(atoms)):
			mapped_atoms = aux_mapped_atoms
			result = aux_result
			aux_mapped_atoms = []
			aux_result = []
			for ma_index in range(0, len(mapped_atoms)):
				mapping_atom_list = self.get_atom_mapping(mapped_atoms[ma_index][index], data_base)
				if (not mapping_atom_list is None):
					for mapping_atom in mapping_atom_list:
						other_mapping = copy.deepcopy(result[ma_index])
						other_mapping.append(mapping_atom)
						aux_result.append(other_mapping)
						cloned_mapped_atoms = copy.deepcopy(mapped_atoms[ma_index])
						for otherAtom in cloned_mapped_atoms:
							otherAtom.map(mapping_atom)
						aux_mapped_atoms.append(cloned_mapped_atoms)

		return aux_result