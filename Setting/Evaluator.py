class Evaluator:
	def __init__(self, ground_truth = {}, prediction_values = []):
		self._ground_truth = ground_truth
		self._predictions = self._get_predictions(prediction_values)

	def _get_predictions(self, prediction_values):
		predictions = {}
		for key in self._ground_truth.keys():
			predictions[key] = False

		for item in prediction_values:
			predictions[item] = True
			#print('hola')

		return predictions

	def evaluate(self):
		fp=0
		vp=0
		vn=0
		fn=0
		for key in self._predictions.keys():
			#print('prediccion:', key)
			pred = self._predictions[key]
			#print('pred:', pred)
			gt = self._ground_truth[key]
			#print('gt:', gt)

			if (pred and gt):
				vp = vp + 1
			elif (pred and (not gt)):
				fp = fp + 1
			elif ((not pred) and (not gt)):
				vn = vn + 1
			elif ((not pred) and gt):
				fn = fn + 1
		precision = 0
		recall = 0
		if((vp + fp) != 0):
			precision = vp / (vp + fp)
		if((vp + fn) != 0):
			recall = vp / (vp + fn)

		#if precision == 0:
		#	print('vp', vp)
		#	print('fp', fp)

		return {"fn": fn, "tn": vn, "tp": vp, "fp": fp, "precision" : precision, "recall" : recall}