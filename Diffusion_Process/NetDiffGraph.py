import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Diffusion_Process.NetDiffNode import NetDiffNode
from Diffusion_Process.NetDiffEdge import NetDiffEdge
from Diffusion_Process.NetDiffGraphElement import NetDiffGraphElement

class NetDiffGraph(NetDiffGraphElement):

	def __init__(self, id, nodes, edges):
		self._id = id
		self._netDiffNodes = []
		self._netDiffEdges = []
		for node in nodes:
			self._netDiffNodes.append(node)
		for edge in edges:
			self._netDiffEdges.append(edge)

	def to_json_string(self):
		result = '{"nodes": ['
		for node in self._netDiffNodes:
			result = result + node.to_json_string() + ","
		result = result[: (len(result) - 1)]
		result = result + '], "edges": ['
		#result = result + '], "links": ['

		for edge in self._netDiffEdges:
			result = result + edge.to_json_string() + ","

		result = result[: (len(result) - 1)]
		result = result + ']}'

		return result

	def get_labels():
		return NetDiffGraph._labels

	def get_components(self):
		return self._netDiffNodes + self._netDiffEdges

	def getNodes(self):
		return self._netDiffNodes

	def add_node(self, node):
		if not node in self._netDiffNodes:
			self._netDiffNodes.append(node)
	
	def getEdges(self):
		return self._netDiffEdges

	def add_edge(self, edge):
		if not edge in self._netDiffEdges:
			self._netDiffEdges.append(edge)

	def getId(self):
		return self._id

	def __str__(self):
		return self._id

	def get_neighbours(self, node):
		result = []

		for edge in self._netDiffEdges:
			if (edge.getTarget() == node.getId()):
				result.append(NetDiffNode(edge.getSource()))
			elif (edge.getSource() == node.getId()):
				result.append(NetDiffNode(edge.getTarget()))

		return result

