from FakeNewsData.DatasetCSV import DatasetCSV

class DatasetCSVLiar(DatasetCSV):

	def __init__(self):
		loc = '../Datasets/Fake News/liar_dataset/train.tsv'
		super().__init__(loc, 2, 1,'\t', False)

	def _is_positive_label(self, label):
		return label in ['pants-fire', 'false', 'barely-true', 'half-true', 'mostly-true']
	
	def _is_negative_label(self, label):
		return label in ['true']