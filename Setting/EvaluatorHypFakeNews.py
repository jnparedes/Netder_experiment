from Evaluator import Evaluator

class EvaluatorHypFakeNews(Evaluator):

	def __init__(self, ground_truth = {}, prediction_values = []):
		super().__init__(ground_truth)
		self._predictions = self.get_predictions(prediction_values)

	def get_predictions(self, prediction_values):
		predictions = {}
		for key in self._ground_truth.keys():
			predictions[key] = False

		for item in prediction_values:
			for key in item.keys():
				predictions[int(item[key].getId())] = True

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
		if((vp + fp) != 0):
			precision = vp / (vp + fp)
		if((vp + fn) != 0):
			recall = vp / (vp + fn)
		return {"precision" : precision, "recall" : recall}