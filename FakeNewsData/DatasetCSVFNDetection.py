from DatasetCSV import DatasetCSV
class DatasetCSVFNDetection(DatasetCSV):

	def __init__(self):
		loc = 'C:/Users/54934/Documents/Datasets/Fake News/fake-news-detection/data.csv'
		super().__init__(loc, 2, 3)

	def _is_positive_label(self, label):
		return label == '1'
	
	def _is_negative_label(self, label):
		return label == '0'