import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from FakeNewsData.Dataset import Dataset

class DatasetTextFiles(Dataset):

	def __init__(self, base_loc, content_label_pair_loc):
		super().__init__(base_loc)
		self._content_label_pair_loc = content_label_pair_loc


	def _load_dataset(self):
		content = []
		ground_truth = []
		for content_loc,label in self._content_label_pair_loc:
			location_list = os.listdir(self._location + content_loc)
			for location in location_list:
				with open(self._location + content_loc + '/' + location, 'r', encoding='utf-8') as file:
					content.append(file.read()[:self._limit_item])
					ground_truth.append(label)
		return (content, ground_truth)

	def _load_data(self):
		content, ground_truth = self._load_dataset()
		return content

	def get_ground_truth(self):
		content, ground_truth = self._load_dataset()
		return ground_truth
