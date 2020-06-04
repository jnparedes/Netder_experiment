import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import portion
from Diffusion_Process.NetDiffGraph import NetDiffGraph
from Diffusion_Process.NetDiffNode import NetDiffNode
from Diffusion_Process.NetDiffEdge import NetDiffEdge

class NetCompTarget:

	def __init__(self, component, label = None, interval = None):
		self._component = component
		self._label = label
		self._interval = interval

	def getBound(self):
		return self._interval

	def getLabel(self):
		return self._label

	def getComponent(self):
		return self._component

	def __str__(self):
		return str(self._component) + '\n' + str(self._label) + '\n' + str(self._interval)