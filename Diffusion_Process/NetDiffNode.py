import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import random
from Diffusion_Process.NetDiffGraphElement import NetDiffGraphElement

class NetDiffNode(NetDiffGraphElement):

	def __init__(self, id):
		self._id = id
		self._color = "blue"

	def get_labels():
		return NetDiffNode._labels

	def __str__(self):
		return 'node(' + self._id + ')'

	def to_json_string(self):
		#if random.randint(1, 50) == 1:
			#self._color = "red"
		return '{"id":"' + str(self._id) + '", "label": "' + str(self._id) + '", "color": "' + self._color + '" }'
		#return '{"id":"' + str(self._id) + '" }'

	def set_color(self, color):
		self._color = color

	def get_color(self):
		return self._color

	def getId(self):
		return self._id

	def __eq__(self, node):
		result = False
		if isinstance(self, type(node)):
			result = self is node

			result = result or (self._id == node.getId())

		return result