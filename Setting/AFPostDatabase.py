from abc import ABC
import random
import copy
import portion
from Diffusion_Process.NLocalLabel import NLocalLabel
from Diffusion_Process.NetDiffFact import NetDiffFact
from Diffusion_Process.NetDiffNode import NetDiffNode
from Ontological.PredictionsFakeNewsRob import PredictionsFakeNewsRob
from CFPublicationFN import CFPublicationFN
from CFPublicationRN import CFPublicationRN
from SocialBotnet import SocialBotnet

class AFPostDatabase(ABC):

	def __init__(self, net_diff_graph, dataset, setting_values = None):
		self._net_diff_graph = net_diff_graph
		self._af_publications = []
		self._hist_publications = []
		self._predictions = [PredictionsFakeNewsRob('pre_hyp_fakenews', setting_values['results_loc'], float(setting_values['fk_threshold'])), PredictionsFakeNewsRob('pre_hyp_fakenews2', setting_values['results_loc'], 0.5)]
		self._dataset = dataset
		self._tmax = int(setting_values["tmax"])
		self._id_posts = []
		self._malicious_prop = float(setting_values["malicious_prop"])
		self._social_botnets = []
		sb_prob = float(setting_values["sb_prob"])
		cant_botnet = int(setting_values["cant_botnet"])
		fn_prob = float(setting_values["fn_prob"])
		for x in range(cant_botnet):
			self._social_botnets.append(SocialBotnet(dataset, fn_prob))
		
		nodes = copy.deepcopy(net_diff_graph.getNodes())
		random.shuffle(nodes)
		index = 0
		cant_mal_nodes = int(len(nodes) * self._malicious_prop)
		for node in nodes:
			af_publication = None
			if index < cant_mal_nodes:
				new_post_prob_mal = float(setting_values["new_post_prob_mal"])
				if random.random() < sb_prob:
					sb_index = random.randint(0, len(self._social_botnets) - 1)
					af_publication = CFPublicationFN(node, dataset, self, fn_prob, new_post_prob_mal, self._social_botnets[sb_index])
				else:
					af_publication = CFPublicationFN(node, dataset, self, fn_prob, new_post_prob_mal)
			else:
				neighbours = net_diff_graph.get_neighbours(node)
				new_post_prob_no_mal = float(setting_values["new_post_prob_no_mal"])
				share_post_prob = float(setting_values["share_post_prob"])
				af_publication = CFPublicationRN(node, neighbours, self, dataset, new_post_prob_no_mal, share_post_prob)
			
			self._af_publications.append(af_publication)
			index += 1

		#self.set_setting_values(setting_values)

	def get_database(self):
		result = {}
		atoms = []
		id_posts = []
		facts = []
		publications = {}
		for af_publication in self._af_publications:
			post = af_publication.get_publication()
			if not post is None:
				atoms.append(post)
				id_post = post.get_terms()[1].getValue()
				node = post.get_terms()[0].getId()
				publications[node] = id_post
				#category = self._dataset.get_category(id_post)
				category = af_publication.get_dominant_category(len(id_posts) + 1)
				nlabel = NLocalLabel(category)
				facts.append(NetDiffFact(NetDiffNode(node), nlabel, portion.closed(1, 1), 0, self._tmax))
				exists = False
				for posts in self._id_posts:
					if id_post in posts:
						exists = True
						break
				if (not exists) and (not id_post in id_posts):
					id_posts.append(id_post)
		self._hist_publications.append(publications)
		self._id_posts.append(id_posts)
		news_atoms = []
		for pred in self._predictions:
			news_atoms = news_atoms + pred.get_atoms(id_posts)
		atoms = atoms + news_atoms
		
		result['ont_db'] = atoms
		result['net_db'] = facts

		return result

	def _get_af_publication(self, node):
		result = None
		for af_publication in self._af_publications:
			if af_publication.get_node() == node:
				result = af_publication
				break

		return result

	def get_random_pub_index(self, node):
		result = None
		af_publication = self._get_af_publication(node)
		if not af_publication is None:
			result = af_publication.get_random_pub_index()

		return result

	def get_dominant_category(self, node, time):
		result = None
		af_publication = self._get_af_publication(node)
		if not af_publication is None:
			result = af_publication.get_dominant_category(time)

		return result

	def get_af_publications(self):
		return self._af_publications

	def get_news(self):
		return self._id_posts

	def get_hist_publications(self):
		return self._hist_publications

	def get_malicious(self):
		nodes = []
		for index in range(int(len(self._af_publications) * self._malicious_prop)):
			nodes.append(self._af_publications[index].get_node().getId())

		return nodes

	def get_nodes_id(self):
		nodes = []
		for af_publication in self._af_publications:
			nodes.append(af_publication.get_node().getId())

		return nodes

	def get_publication(self, node, category):
		result = None
		for index in range(len(self._hist_publications) - 1):
			if node in self._hist_publications[index].keys():
				if self._dataset.get_category(self._hist_publications[index][node]) == category:
					result = self._hist_publications[index][node]
					break

		return result
	
	def get_members_in_botnets(self):
		result = []
		for botnet in self._social_botnets:
			result.append(botnet.get_members())

		return result

	def set_setting_values(self, setting_values):
		self._predictions.set_results_loc(setting_values['results_loc'])
		self._predictions.set_fk_threshold(float(setting_values['fk_threshold']))

	def get_dataset(self):
		return self._dataset



