from Predictor import Predictor
import requests,json, os
import lxml.html

class PredictorFakeNewsXcheck(Predictor):
	
	def __init__(self, umbral, url_base, results_loc):
		super().__init__(10, umbral, results_loc, "log.txt")
		self._url_base = url_base

	def _get_prediction(self, item):
		client = requests.session()
		req = client.get(self._url_base)

		lxml_mysite = lxml.html.fromstring(req.text)
		csrf  = lxml_mysite.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]

		item = item.replace('"', '')
		myitem = item.encode("ascii", "replace")

		print(myitem)
		info = {'Website':'', 'KeyWord':'', 'ArticleS': 'Article', 'Article': myitem, 'csrfmiddlewaretoken' : csrf}
		#info = '{"Website":"", "KeyWord":"", "ArticleS": "Article", "Article":' + item + ', "csrfmiddlewaretoken" :' + csrf + '}'
		response = client.post(self._url_base, data = info)

		lxml_mysite = lxml.html.fromstring(response.text)
		pred = lxml_mysite.xpath('//h3')[1]
		print(item)
		print(pred.text.split())
		pred_value = float(pred.text.split()[0])
		
		print(pred_value / 100)
		print(1 - pred_value / 100)
		print(len(item))
		print(response.status_code)
		return json.loads('{"fake_news_prediction":' + str(1 - (pred_value / 100) ) + '}')

	def last_predictions(self):
		resultado = []
		with open(self._results_loc) as json_file:
			data = json.load(json_file)
			for pred in data:
				if (pred['fake_news_prediction'] >= self._umbral):
					resultado.append(True)
				else:
					resultado.append(False)
		return resultado