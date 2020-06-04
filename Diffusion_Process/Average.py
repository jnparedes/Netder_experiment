import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Diffusion_Process.AbstractAgregationFunction import AbstractAgregationFunction
import portion

class Average(AbstractAgregationFunction):

	def aggregate(self, bounds):
		result = portion.closed(0, 1)
		lower = 0
		upper = 0
		for bound in bounds:
			lower = lower + bound.lower
			upper = upper + bound.upper
		if len(bounds) > 0:
			lower = lower / len(bounds)
			upper = upper / len(bounds)
		else:
			lower = 0
			upper = 1
		result = portion.closed(lower, upper)
		return result

