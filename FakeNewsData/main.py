import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import requests, csv
from DatasetCSVLiar import DatasetCSVLiar
from PredictorFakeNewsRob import PredictorFakeNewsRob
from PredictorFakeNewsXcheck import PredictorFakeNewsXcheck
from DatasetCSVFNDetection import DatasetCSVFNDetection
from DatasetTextDB import DatasetTextDB
from DatasetTextFilesFakeNews import DatasetTextFilesFakeNews
from DatasetTextFilesCelebrity import DatasetTextFilesCelebrity
from DatasetCSVFND import DatasetCSVFND
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf
import lxml.html
import json

url_base = 'https://robinho.fakenewsdetector.org/'
#req = requests.get(url_base + 'predict?title=prueba&url=https://example.com&content=un contenido para probar')
#req = requests.get(url_base + 'predict?title=&url=&content=un contenido para probar')
#print(req.text)

#dataset = DatasetCSVLiar()
#predictor = PredictorFakeNewsRob(0.2, 'https://robinho.fakenewsdetector.org/predict', 'results/res.json')
#predictor.do_predictions(dataset.get_data())
#print(predictor.evaluate(dataset.get_ground_truth()))
#dataset = DatasetCSVFNDetection()
#dataset = DatasetTextDB()
#predictor = PredictorFakeNewsRob(0.9, 'https://robinho.fakenewsdetector.org/predict', 'results/res_FND.json')
#print(len(dataset.get_data()))
#print(dataset.get_data()[0])
#print(len(dataset.get_data()[1]))
#predictor.do_predictions(dataset.get_data()[1:])
#print(predictor.evaluate(dataset.get_ground_truth()))
#dataset = DatasetCSVFND()

''''
url_test = 'http://localhost:8000/'

client = requests.session()
req = client.get(url_test)

lxml_mysite = lxml.html.fromstring(req.text)
csrf  = lxml_mysite.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]

info = {'Website':'', 'KeyWord':'', 'ArticleS':'Article','Article':'Brexit day one: Johnson goes for broke with hardline trade deal', 'csrfmiddlewaretoken' : csrf}

req2 = client.post(url_test, data = info)
lxml_mysite = lxml.html.fromstring(req2.text)
pred = lxml_mysite.xpath('//h3')[1]
print(req2.text)
print(pred.text.split())
print(float(pred.text.split()[0]))

print(json.loads('{"fake_news_prediction": 1}'))
'''
#predictor = PredictorFakeNewsXcheck(0.2, 'http://localhost:8000/', 'results/Xcheck/res_TextDB.json')
predictor = PredictorFakeNewsRob(0.2, 'https://robinho.fakenewsdetector.org/predict', 'results/res_Liar2.json')

dataset = DatasetCSVLiar()

'''
for data in dataset.get_data():
	if data == '':
		print('Hola')

resultado = []
with open('C:/Users/54934/Documents/Datasets/Fake News/fake-news-detection/data.csv', newline='', encoding='utf-8') as csvfile:
	spamreader = csv.reader(csvfile, delimiter = ',')
	for row in spamreader:
		if(row[2] != '' and (row[3] == '1' or row[3] == '0' or row[3] == 'Label')):
			resultado.append(row)

with open('C:/Users/54934/Documents/Datasets/Fake News/fake-news-detection/data - Copy.csv', 'w', newline='', encoding='utf-8') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter = ',')
	spamwriter.writerows(resultado)'''

#print(dataset.get_data()[268])
predictor.do_predictions(dataset.get_data())
print(len(predictor.last_predictions()))
print(len(dataset.get_data()))
print(len(dataset.get_ground_truth()))
#print(predictor.evaluate(dataset.get_ground_truth()))

#mysite = urllib.request.urlopen('http://www.google.com').read()
#lxml_mysite = lxml.html.fromstring(req.text)
#description = lxml_mysite.xpath("//form") # meta tag description
#print(description[0])

#for element in description[0].iter(tag=etree.Element):
#	print("%s - %s" % (element.tag, element.text))
#print(csrf.get_token())