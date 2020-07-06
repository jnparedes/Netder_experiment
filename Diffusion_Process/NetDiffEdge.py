import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Diffusion_Process.NetDiffGraphElement import NetDiffGraphElement

class NetDiffEdge(NetDiffGraphElement):

	def __init__(self, source, target):
		self._source = source
		self._target = target
		self._id = "(" + source + ',' + target + ')'
	
	def get_labels():
		return NetDiffEdge._labels

	def __str__(self):
		return 'edge' + self._id
	
	def to_json_string(self):
		return '{"id":"'+ str(self._id) +'", "from":'+ str(self._source) + ', "to":' + str(self._target) + ', "color": "black" ' + '}'
		#return '{"from":"'+ str(self._source) + '", "to":"' + str(self._target) + '"}'
	def getSource(self):
		return self._source

	def getTarget(self):
		return self._target

	def getId(self):
		return self._id

	def __eq__(self, edge):
		result = False
		if isinstance(self, type(edge)):
			result = self is edge

			result = result or (self._source == edge.getSource() and self._target == edge.getTarget())

		return result
