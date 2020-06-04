from DatasetCSV import DatasetCSV
class DatasetTextDB(DatasetCSV):

	def __init__(self):
		loc = 'C:/Users/54934/Documents/Datasets/Fake News/textdb3/fake_or_real_news.csv'
		super().__init__(loc, 2, 3)

	def _is_positive_label(self, label):
		return label == 'FAKE'
	
	def _is_negative_label(self, label):
		return label == 'REAL'