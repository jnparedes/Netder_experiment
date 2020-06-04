from DatasetTextFiles import DatasetTextFiles

class DatasetTextFilesFakeNews(DatasetTextFiles):

	def __init__(self):
		super().__init__('C:/Users/54934/Documents/Datasets/Fake News/fakenewsdataset/training/training/fakeNewsDataset',[('/fake', True), ('/legit', False)])