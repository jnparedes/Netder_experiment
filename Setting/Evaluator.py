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
			pred = self._predictions[key]
			gt = self._ground_truth[key]

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
		f1 = None
		if((vp + fp) != 0):
			precision = vp / (vp + fp)
		else:
			precision = None
		if((vp + fn) != 0):
			recall = vp / (vp + fn)
		else:
			recall = None
		if (not precision is None) and (not recall is None):
			if precision != 0 or recall != 0:
				f1 = 2 * (precision * recall) / (precision + recall)

		return {"fn": fn, "tn": vn, "tp": vp, "fp": fp, "precision" : precision, "recall" : recall, 'f1': f1}