#from abc import ABC

#class DatasetCSV(ABC, Dataset):
import csv
from FakeNewsData.AugmentedDataset import AugmentedDataset
from abc import abstractmethod

class DatasetCSV(AugmentedDataset):
	def __init__(self, location, data_col, ground_truth_col, delimiter=',', headers = True):
		super().__init__(location)
		self._id_col = 0
		self._data_col = data_col
		self._ground_truth_col = ground_truth_col
		self._delimiter = delimiter
		self._headers = headers
	
	def _load_data(self):
		resultado = {}
		with open(self._location, newline='', encoding='utf-8') as csvfile:
			spamreader = csv.reader(csvfile, delimiter = self._delimiter)
			data = list(spamreader)
			if self._headers:
				data = data[1:]
			for row in data:
				if(self._limit_item != None):
					item = row[self._data_col][:self._limit_item]
				else:
					item = row[self._data_col]
				resultado[row[self._id_col]] = item
		
		return resultado

	def get_ground_truth(self):
		resultado = {}
		contador = 0
		with open(self._location, newline='', encoding='utf-8') as csvfile:
			spamreader = csv.reader(csvfile, delimiter = self._delimiter)
			for row in spamreader:
				#if(row[self._ground_truth_col] in ['pants-fire','false','barely-true']):
				if(self._is_positive_label(row[self._ground_truth_col])):
					resultado[row[self._id_col]] = True
					#resultado.append(True)
				#elif (row[self._ground_truth_col] in ['half-true','mostly-true','true']):
				elif(self._is_negative_label(row[self._ground_truth_col])):
					#resultado.append(False)
					resultado[row[self._id_col]] = False
				else:
					print('hay un problema')
					print(row[self._ground_truth_col])
					print(contador)
				contador = contador + 1
		return resultado

	@abstractmethod
	def _is_positive_label(self, label):
		pass
	
	@abstractmethod
	def _is_negative_label(self, label):
		pass