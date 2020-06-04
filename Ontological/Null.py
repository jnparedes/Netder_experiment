import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Ontological.Term import Term
from Ontological.Constant import Constant

class Null(Term):
	_counter = 0
	
	def __init__(self):
		super().__init__('z' + str(Null._counter), 'z' + str(Null._counter))
		Null._counter = Null._counter + 1

	def can_be_instanced(self):
		return True

