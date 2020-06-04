from abc import ABC,abstractmethod
import json

class Predictor(ABC):
	
	def __init__(self, step, umbral ,results_loc, log_loc):
		self._step = step
		self._results_loc = results_loc
		self._log_loc = log_loc
		self._umbral = umbral
	
	@abstractmethod
	def _get_prediction(self, item):
		pass
	
	def _save_data(self, data):
		with open(self._results_loc, 'r+') as json_file:
			json_file.seek(0) #ensure you're at the start of the file..
			first_char = json_file.read(1) #get the first character
			if (not first_char):
				json_file.seek(0)
				json.dump(data, json_file)
			else:
				json_file.seek(0)
				old_data = json.load(json_file)
				json_file.seek(0)
				json.dump(old_data + data, json_file)

	def _load_data(self):
		with open(self._results_loc) as json_file:
			return json.load(json_file)

	@abstractmethod
	def last_predictions():
		pass

	def _save_progress(self, progress):
		with open(self._log_loc, 'a+') as file:
			file.write(str(progress)+'\n')

	def do_predictions(self, data, offset = 0):
		res = []
		counter = 0
		progress = 0
		for key in data.keys():
			if (offset == 0):
				pred = self._get_prediction(data[key])
				pred['id'] = key
				res.append(pred)
				counter = counter + 1
				progress = progress + 1
				if (counter == self._step):
					self._save_data(res)
					self._save_progress(progress)
					res = []
					counter = 0
			else:
				offset = offset - 1
			print('progress: ' + str(progress))
		if (len(res) > 0):
			self._save_data(res)
			self._save_progress(progress)

	def evaluate(self, ground_truth, predictions=None):
		if (predictions == None):
			predictions = self.last_predictions()
		fp=0
		vp=0
		vn=0
		fn=0
		iterator = iter(ground_truth)
		for pred in predictions:
			gt = next(iterator)
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
	