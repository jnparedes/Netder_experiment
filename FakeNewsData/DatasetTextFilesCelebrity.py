import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from FakeNewsData.DatasetTextFiles import DatasetTextFiles

class DatasetTextFilesCelebrity(DatasetTextFiles):

	def __init__(self):
		super().__init__('C:/Users/54934/Documents/Datasets/Fake News/fakenewsdataset/training/training/celebrityDataset',[('/fake', True), ('/legit', False)])