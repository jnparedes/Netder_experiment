import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DatasetCSVLiar import DatasetCSVLiar
from DatasetCSVFND import DatasetCSVFND
from DatasetCSVFNDetection import DatasetCSVFNDetection
from DatasetTextDB import DatasetTextDB
from DatasetTextFilesCelebrity import DatasetTextFilesCelebrity
from DatasetTextFilesFakeNews import DatasetTextFilesFakeNews
from PredictorFakeNewsRob import PredictorFakeNewsRob
from PredictorFakeNewsXcheck import PredictorFakeNewsXcheck
from datetime import datetime

dataset = DatasetTextFilesCelebrity()
print('len(dataset)')
print(len(dataset.get_data()))

inicio = datetime.now()
#predictor = PredictorFakeNewsRob(0.9, 'https://robinho.fakenewsdetector.org/predict', 'results/res_Liar.json')
#predictor = PredictorFakeNewsXcheck(0.9, 'http://localhost:8000/', 'results/Xcheck/res_FND.json')
#predictor.do_predictions(dataset.get_data())
#print(predictor.evaluate(dataset.get_ground_truth()))
#print(len(predictor.last_predictions()))

fin = datetime.now()
print(fin - inicio)