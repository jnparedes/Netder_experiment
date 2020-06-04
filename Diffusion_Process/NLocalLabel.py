import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Diffusion_Process.Label import Label

class NLocalLabel(Label):

	def __init__(self, value):
		super().__init__(value)