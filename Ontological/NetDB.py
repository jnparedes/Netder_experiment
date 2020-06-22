import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Diffusion_Process.NetDiffGraph import NetDiffGraph
from Diffusion_Process.NetDiffNode import NetDiffNode
from Diffusion_Process.NetDiffEdge import NetDiffEdge
from Ontological.Constant import Constant
from Ontological.Atom import Atom

class NetDB:

	def __init__(self, net_diff_graph = NetDiffGraph('graph', [], []), diff_facts = []):
		self._net_diff_graph = net_diff_graph
		self._load_comp_atoms()
		self._diff_facts = diff_facts

	def _load_comp_atoms(self):
		self._comp_atoms = {}
		self._comp_atoms['node'] = []
		self._comp_atoms['edge'] = []
		for node in self._net_diff_graph.getNodes():
			self._comp_atoms['node'].append(Atom('node', [Constant(node.getId())]))

		for edge in self._net_diff_graph.getEdges():
			self._comp_atoms['edge'].append(Atom('edge', [Constant(edge.getSource()), Constant(edge.getTarget())]))

	def get_net_diff_graph(self):
		return self._net_diff_graph

	def get_net_data(self):
		result = []
		for node in self._net_diff_graph.getNodes():
			result.append(Atom('node', [Constant(node.getId())]))

		for edge in self._net_diff_graph.getEdges():
			result.append(Atom('edge', [Constant(edge.getSource()), Constant(edge.getTarget())]))			
		
		return result

	def get_net_diff_facts(self):
		return self._diff_facts

	def get_comp_from_atom(self, atom):
		result = None
		node = self._get_node_from_atom(atom)
		edge = self._get_edge_from_atom(atom)
		if not node is None:
			result = node
		elif not edge is None:
			result = edge

		return result

	def _get_node_from_atom(self, atom):
		result = None
		if atom.getId() == 'node':
			result = NetDiffNode(atom.get_terms()[0].getValue())

		return result

	def _get_edge_from_atom(self, atom):
		result = None
		if atom.getId() == 'edge':
			result = NetDiffEdge(atom.get_terms()[0].getValue(), atom.get_terms()[1].getValue())

		return result

	def add_knowledge(self, knowledge, time):
		for nct in knowledge:
			node = self._get_node_from_atom(nct.getComponent())
			edge = self._get_edge_from_atom(nct.getComponent())
			if (not node is None):
				self._net_diff_graph.add_node(node)
			elif (not edge is None):
				self._net_diff_graph.add_edge(edge)
		self._load_comp_atoms()

	def add_facts(self, facts):
		self._diff_facts = self._diff_facts + facts

	def set_facts(self, facts):
		self._diff_facts = facts
	
	def get_comp_from_pred(self, pred):
		result = []
		if pred in self._comp_atoms.keys():
			result = self._comp_atoms[pred]

		return result
