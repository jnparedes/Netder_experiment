import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import copy
from Ontological.NetDB import NetDB
from Ontological.Variable import Variable
from Ontological.Constant import Constant
from Ontological.Atom import Atom
from Ontological.OntDB import OntDB

class NetDERKB:

	def __init__(self, ont_data = [], net_db= NetDB(), netder_tgds=[], netder_egds = [], netdiff_lrules=[], netdiff_grules=[]):
		self._ont_db = OntDB()
		self.add_ont_knowledge(ont_data)
		self._net_db = net_db
		self._netder_tgds = netder_tgds
		self._netder_egds = netder_egds
		self._netdiff_lrules = netdiff_lrules
		self._netdiff_grules = netdiff_grules

	def add_ont_knowledge(self, atoms):
		success = False
		copy_atoms = copy.deepcopy(atoms)
		index = 0
		for atom in copy_atoms:
			result = self._ont_db.add_atom(atom)
			success = success or result

		return success

	def add_net_knowledge(self, knowledge, time):
		self._net_db.add_knowledge(knowledge, time)

	def add_facts(self, facts):
		self._net_db.add_facts(facts)

	def get_net_diff_facts(self):
		return self._net_db.get_net_diff_facts()

	def get_ont_db(self):
		return self._ont_db

	def get_net_data(self):
		return self._net_db.get_net_data()

	def get_comp_from_atom(self, atom):
		return self._net_db.get_comp_from_atom(atom)

	def get_netder_egds(self):
		return self._netder_egds

	def get_netder_tgds(self):
		return self._netder_tgds

	def get_net_diff_lrules(self):
		return self._netdiff_lrules

	def get_net_diff_grules(self):
		return self._netdiff_grules

	def get_net_diff_graph(self):
		return self._net_db.get_net_diff_graph()

	def apply_map(self, mapping):
		self._ont_db.apply_mapping(mapping)

	def get_data_from_pred(self, pred):
		return self._ont_db.get_atoms_from_pred(pred) + self._net_db.get_comp_from_pred(pred)


	def remove_atoms_from_pred(self, pred):
		self._ont_db.remove_atoms_from_pred(pred)

	def get_net_db(self):
		return self._net_db