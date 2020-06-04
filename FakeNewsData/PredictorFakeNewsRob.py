from Predictor import Predictor
import requests,json, os

class PredictorFakeNewsRob(Predictor):
	
	def __init__(self, umbral, url_base, results_loc):
		super().__init__(10, umbral, results_loc, "log.txt")
		self._url_base = url_base

	def _get_prediction(self, item):
		req = requests.get(self._url_base + '?title=&url=&content=' + item)
		print(len(item))
		print(req.status_code)
		return req.json()

	def last_predictions(self):
		resultado = []
		with open(self._results_loc) as json_file:
			data = json.load(json_file)
			for pred in data:
				if (pred['predictions']['fake_news'] >= self._umbral):
					resultado.append(True)
				else:
					resultado.append(False)
		return resultado