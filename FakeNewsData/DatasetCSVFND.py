from DatasetCSV import DatasetCSV
class DatasetCSVFND(DatasetCSV):

	def __init__(self):
		loc = 'C:/Users/54934/Documents/Datasets/Fake News/fake-news-detection-dataset/train.csv'
		super().__init__(loc, 0, 1)

	def _is_positive_label(self, label):
		return label.lower() == 'true'
	
	def _is_negative_label(self, label):
		return label.lower() == 'false'