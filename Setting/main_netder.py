import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from datetime import datetime
import csv
import portion
import copy
import json
from FakeNewsData.AugmentedDatasetCSVLiar import AugmentedDatasetCSVLiar
from FakeNewsData.DatasetCSVLiar import DatasetCSVLiar
from FakeNewsData.AugmentedDatasetTextFilesCelebrity import AugmentedDatasetTextFilesCelebrity
from AFPostDatabase import AFPostDatabase
from EarlyPoster import EarlyPoster
from Closer import Closer
from NewsCategory import NewsCategory
from Evaluator import Evaluator
from Diffusion_Process.NetDiffNode import NetDiffNode
from Diffusion_Process.NetDiffEdge import NetDiffEdge
from Diffusion_Process.NetDiffGraph import NetDiffGraph
from Diffusion_Process.NetDiffFact import NetDiffFact
from Diffusion_Process.NLocalLabel import NLocalLabel
from Diffusion_Process.GlobalLabel import GlobalLabel
from Diffusion_Process.NetDiffLocalRule import NetDiffLocalRule
from Diffusion_Process.NetDiffGlobalRule import NetDiffGlobalRule
from Diffusion_Process.Average import Average
from Diffusion_Process.Tipping import Tipping
from Diffusion_Process.EnhancedTipping import EnhancedTipping
from Ontological.NetDERKB import NetDERKB
from Ontological.NetDB import NetDB
from Ontological.NetDERChase import NetDERChase
from Ontological.NetDERQuery import NetDERQuery
from Ontological.NetDERTGD import NetDERTGD
from Ontological.NetDEREGD import NetDEREGD
from Ontological.Atom import Atom
from Ontological.GRE import GRE
from Ontological.Distinct import Distinct
from Ontological.Variable import Variable
from Ontological.Constant import Constant
from Ontological.PredictionsFakeNewsRob import PredictionsFakeNewsRob
from Ontological.NetCompTarget import NetCompTarget

def get_csv_headers(csv_source):
	with open(csv_source, 'r', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		headers = reader.fieldnames

	return headers

def save_csv(csv_source, data):
	#fieldnames = get_csv_headers(csv_source)
	fieldnames = {}
	for key in data.keys():
		fieldnames[key] = key
	fieldnames = list(data.keys())
	'''
	read_data = []
	with open(csv_source, 'w', newline='') as csvfile:
		pass
	with open(csv_source, 'r', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		read_data = list(reader)
	if len(read_data) == 0:
		with open(csv_source, 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
			writer.writerow(fieldnames)
			print('holaaaaaaa')
	else:
		fieldnames = get_csv_headers(csv_source)'''
	with open(csv_source, 'a+', newline='') as csvfile:
		#reader = csv.DictReader(csvfile, fieldnames = fieldnames)
		#read_data = list(reader)
		read_data = []
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
		if os.stat(csv_source).st_size > 0:
			reader = csv.DictReader(csvfile, fieldnames = fieldnames)
			read_data = list(reader)
		else:
			writer.writeheader()
		writer.writerows(read_data)
		writer.writerow(data)

'''
setting_values = {'fk_threshold': 0.3, 'tmax': 2, 'time_sim': 15, 'trending interval': portion.closed(0.5, 1),
					'cant_botnet': 1, 'sb_prob': 0.5, 'fn_prob': 0.1, 'malicious_prop': 0.25,
					'new_post_prob_mal': 0.1, 'new_post_prob_no_mal': 0.01, 'share_post_prob': 0.1,
					'csv_graph_location': '../graph_data/graph(n=1000, e=2000).csv', 
					'results_loc': '../FakeNewsData/results/res_Liar.json'}'''
'''
setting_values = {'fk_threshold': 0.3, 'tmax': 2, 'time_sim': 15, 'trending_interval_lower': 0.5,
					'trending_interval_upper': 1, 'cant_botnet': 5, 'sb_prob': 1, 'fn_prob': 0.1, 'malicious_prop': 0.25,
					'new_post_prob_mal': 0.3, 'new_post_prob_no_mal': 0.01, 'share_post_prob': 0.99,
					'csv_graph_location': '../graph_data/graph(n=150, e=495).csv', 
					'results_loc': '../FakeNewsData/results/res_Liar.json'}'''

setting_values_collection = None
with open('../setting_values.csv', newline='') as csvfile:
	setting_values_collection = list(csv.DictReader(csvfile))

inicio = datetime.now()
setting_counter = 1

for setting_values in setting_values_collection:
	result_eval = {}
	result_eval["setting"] = setting_values['setting']
	reduced_result_eval = {}
	reduced_result_eval2 = [{},{},{}]
	for header in get_csv_headers('../reduced_result_experiment.csv'):
		for rr in reduced_result_eval2:
			rr[str(header)] = {'total_value': 0, 'total_samples': int(setting_values["cant_run"])}

	for run in range(int(setting_values["cant_run"])):
		detection_times = []
		result_eval["run"] = run + 1
		inicio_setting = datetime.now()
		print('Setting Values Nro:', setting_counter)

		tmax = int(setting_values["tmax"])
		time_sim = int(setting_values["time_sim"])

		fn_dataset = DatasetCSVLiar()
		#fn_dataset = AugmentedDatasetTextFilesCelebrity()
		#nodes = [NetDiffNode('0'), NetDiffNode('1'), NetDiffNode('2'), NetDiffNode('3')]
		#edges = [NetDiffEdge('0', '1'), NetDiffEdge('0', '2'), NetDiffEdge('0', '3'), NetDiffEdge('2', '3')]

		csv_graph_location = setting_values["csv_graph_location"]
		#csv_graph_location = "../graph_data/graph(n=150, e=495).csv"
		#csv_graph_location = "../graph_data/graph(n=1000, e=2000).csv"
		json_graph_location = "graph.json"

		nodes = set()
		edges = set()

		with open(csv_graph_location, newline = '', encoding = 'utf-8') as csvfile:
			spamreader = csv.reader(csvfile, delimiter = ',')
			for row in spamreader:
				nodes.add(row[0])
				nodes.add(row[1])
				edges.add((row[0], row[1]))
		aux_nodes = []
		aux_edges = []
		for node in nodes:
			aux_nodes.append(NetDiffNode(node))
		for (n1, n2) in edges:
			aux_edges.append(NetDiffEdge(n1, n2))

		nodes = aux_nodes
		edges = aux_edges

		graph = NetDiffGraph('graph', nodes, edges)

		posts_db = AFPostDatabase(graph, fn_dataset, setting_values = setting_values)

		ont_db = []
		net_db = []
		inicio_bdb = datetime.now()
		for time in range(time_sim):
			print('time: ', time)
			logic_database = posts_db.get_database()
			ont_db.append(logic_database['ont_db'])
			net_db.append(logic_database['net_db'])
		fin_bdb = datetime.now()

		total_posts = 0
		for posts in posts_db.get_news():
			total_posts = total_posts + len(posts)
		print('total_posts:', total_posts)

		category_nlabels = []
		category_glabels = []
		category_kinds = fn_dataset.get_category_kinds()
		for category in category_kinds:
			category_nlabels.append(NLocalLabel(category))
			category_glabels.append(GlobalLabel('trending(' + category + ')'))

		nodes[0].setLabels(category_nlabels)
		graph.setLabels(category_glabels)

		local_rules = []
		for nlabel in category_nlabels:
			#local_rules.append(NetDiffLocalRule(nlabel, [], 1, [(nlabel, portion.closed(1, 1))], [], Tipping(0.5, portion.closed(1, 1))))
			local_rules.append(NetDiffLocalRule(nlabel, [], 1, [(nlabel, portion.closed(1, 1))], [], EnhancedTipping(0.5, portion.closed(1, 1))))

		global_rules = []
		index = 0
		for glabel in category_glabels:
			global_rules.append(NetDiffGlobalRule(glabel, category_nlabels[index], [], Average()))
			index += 1

		#predictions = PredictionsFakeNewsRob('../FakeNewsData/results/res_TextFilesCelebrity.json')


		#atom1 = Atom('news', [Variable('FN'), Variable('fake_level')])
		#atom2 = GRE(Variable('fake_level'), Constant(0.3))
		atom3 = Atom('user', [Variable('UID')])
		atom4  = Atom('earlyPoster', [Variable('UID'), Variable('FN')])
		atom5 = Atom('hyp_is_resp', [Variable('UID'), Variable('FN1')])
		atom6 = Atom('hyp_is_resp', [Variable('UID'), Variable('FN2')])
		atom7 = Distinct(Variable('FN1'), Variable('FN2'))
		atom8 = Atom('pre_hyp_fakenews', [Variable('FN')])
		atom9 = Atom('hyp_malicious', [Variable('UID1')])
		atom10 = Atom('hyp_malicious', [Variable('UID2')])
		atom11 = Atom('closer', [Variable('UID1'), Variable('UID2')])
		atom12 = Atom('pre_hyp_fakenews2', [Variable('FN')])
		atom13 = Atom('hyp_is_resp', [Variable('UID1'), Variable('FN1')])
		atom14 = Atom('hyp_is_resp', [Variable('UID2'), Variable('FN1')])
		atom15 = Distinct(Variable('UID1'), Variable('UID2'))
		atom16 = Atom('edge', [Variable('UID1'), Variable('UID2')])
		nct1 = NetCompTarget(atom16)


		ont_head1 = Atom('hyp_fakenews', [Variable('FN')])
		ont_head2 = Atom('hyp_is_resp', [Variable('UID'), Variable('FN')])
		ont_head3 = Atom('hyp_malicious', [Variable('UID')])
		ont_head4 = [Atom('hyp_botnet', [Variable('B')]), Atom('member', [Variable('UID1'), Variable('B')]), Atom('member', [Variable('UID2'), Variable('B')])]

		global_conditions = []
		for glabel in category_glabels:
			#global_conditions.append((glabel, portion.closed(0.5, 1)))
			global_conditions.append((glabel, portion.closed(float(setting_values["trending_interval_lower"]), float(setting_values["trending_interval_upper"]))))

		tgds1 = []
		tgds2 = []
		tgds3 = []

		#news(FN, fake_level) ^ (fake_level > \theta_1) -> hyp_fakeNews(FN) : trending(FN)
		#pre_hyp_fakenews(FN) -> hyp_fakeNews(FN) : trending(FN)
		#pre_hyp_fakenews(FN) ^ news_category(FN, C)-> hyp_fakeNews(FN) : trending(C)
		tgd_counter = 0
		for gc in global_conditions:
			#tgds.append(NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom8], ont_head = [ont_head1], global_cond = [gc]))
			news_category_atom = Atom('news_category', [Variable('FN'), Constant(category_kinds[tgd_counter])])
			tgds1.append(NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom8, news_category_atom], ont_head = [ont_head1], global_cond = [gc]))
			tgd_counter += 1

		#hyp_fakeNews(FN) ^ earlyPoster(UID, FN) ^ user(UID, N) -> hyp_is_resp(UID, FN)
		#hyp_fakeNews(FN) ^ earlyPoster(UID, FN) -> hyp_is_resp(UID, FN)

		tgd1 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [ont_head1, atom4], ont_head = [ont_head2])
		tgd_counter += 1

		#(V1) hyp_is_resp(UID, FN1) ^ hyp_is_resp(UID, FN2) ^ (FN1 != FN2) -> hyp_malicious(UID)
		#(V2) hyp_is_resp(UID, FN1) -> hyp_malicious(UID)

		tgd2 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom5, atom6, atom7], ont_head = [ont_head3])
		#tgd2 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom5], ont_head = [ont_head3])
		tgd_counter += 1

		#hyp_malicious(UID1) ^ hyp_malicious(UID2) ^ closer(UID1, UID2) ^ (V > \theta_2) ^ (UID1 != UID2) -> \exists B hyp_botnet(B) ^ member(UID1, B) ^ member(UID2, B)
		tgd3 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom9, atom10, atom11], ont_head = ont_head4)
		#tgd3 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom13, atom14, atom15], ont_head = ont_head4)
		tgd_counter += 1

		tgd4 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom12], ont_head = [ont_head1])
		tgd_counter += 1

		tgd5 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom9, atom10], net_body = [nct1], ont_head = ont_head4)
		tgd_counter += 1

		tgd6 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom5], ont_head = [ont_head3])
		tgd_counter += 1

		tgds1.append(tgd1)
		tgds3.append(tgd1)
		tgds1.append(tgd2)
		tgds3.append(tgd6)
		tgds1.append(tgd4)
		tgds2 = copy.deepcopy(tgds1)
		tgds1.append(tgd3)
		tgds3.append(tgd3)
		tgds2.append(tgd5)
		egds = []
		egd_counter = 0
		#hyp_botnet(B1) ^ hyp_botnet(B2) ^ member(UID, B1) ^ member(UID, B2) ->  B1 = B2
		egd1 = NetDEREGD(rule_id = 'egd' + str(egd_counter), ont_body = [Atom('member', [Variable('UID'), Variable('B1')]), Atom('member', [Variable('UID'), Variable('B2')])], head = [Variable('B1'), Variable('B2')])

		egds.append(egd1)

		#query1 = NetDERQuery(exist_var = [], ont_cond = [Atom('hyp_fakenews', [Variable('X')]), Atom('hyp_is_resp', [Variable('Y'), Variable('Z')])], time = (2, 2))
		#query1 = NetDERQuery(exist_var = [Variable('B')], ont_cond = [Atom('hyp_fakenews', [Variable('X')]), Atom('hyp_is_resp', [Variable('Y'), Variable('Z')]), Atom('hyp_malicious', [Variable('M')]), Atom('member', [Variable('UID1'), Variable('B')]), Atom('member', [Variable('UID2'), Variable('B')]), Distinct(Variable('UID1'), Variable('UID2'))], time = (2, 2))
		query1 = NetDERQuery(exist_var = [Variable('B')], ont_cond = [Atom('hyp_fakenews', [Variable('X')]), Atom('hyp_is_resp', [Variable('Y'), Variable('Z')]), Atom('hyp_malicious', [Variable('M')]), Atom('member', [Variable('UID1'), Variable('B')]), Atom('member', [Variable('UID2'), Variable('B')]), Distinct(Variable('UID1'), Variable('UID2'))], time = (tmax, tmax))
		#query1 = NetDERQuery(exist_var = [], ont_cond = [Atom('hyp_fakenews', [Variable('X')])], time = (2, 2))
		#query1 = NetDERQuery(exist_var = [Variable('B')], ont_cond = [Atom('member', [Variable('UID1'), Variable('B')]), Atom('member', [Variable('UID2'), Variable('B')]), Distinct(Variable('UID1'), Variable('UID2'))], time = (2, 2))

		news_dataset_ground_truth = fn_dataset.get_ground_truth()

		orig_news_ground_truth_full = []
		index = 0
		for posts_in_time in posts_db.get_news():
			news_ground_truth = {}
			for news in posts_in_time:
				found = False
				for time_gt in orig_news_ground_truth_full:
					if news in time_gt.keys():
						found = True
						break
				if not found:
					news_ground_truth[news] = news_dataset_ground_truth[news]
			orig_news_ground_truth_full.append(news_ground_truth)
			

			index += 1
		
		orig_news1_ground_truth_full = copy.deepcopy(orig_news_ground_truth_full)
		orig_news2_ground_truth_full = copy.deepcopy(orig_news_ground_truth_full)

		index = 0
		malicious = posts_db.get_malicious()
		orig_hyp_is_resp_gt_time = []
		hyp_is_resp_gt_full = {}
		time_log = {'start': None, 'end': None}
		hyp_is_resp_time = {}
		detection_times.append({'name': 'hyp_is_resp_time', 'value': hyp_is_resp_time})
		for hist_pub in posts_db.get_hist_publications():
			hyp_is_resp_gt = {}
			for node in hist_pub.keys():
				label = False
				if node in malicious and news_dataset_ground_truth[hist_pub[node]]:
					label = True
				key = '(' + str(node) + ',' + str(hist_pub[node]) + ')'
				if not key in hyp_is_resp_gt_full.keys():
					hyp_is_resp_gt[key] = label
					if label:
						clone_time_log = copy.deepcopy(time_log)
						clone_time_log['start'] = index
						hyp_is_resp_time[key] = clone_time_log
				
					hyp_is_resp_gt_full[key] = label


			orig_hyp_is_resp_gt_time.append(hyp_is_resp_gt)
			index += 1
		

		orig_hyp_is_mal_gt_time = []
		hyp_is_mal_gt_full = {}
		hyp_is_mal_time = {}
		detection_times.append({'name': 'hyp_is_mal_time', 'value': hyp_is_mal_time})
		malicious = posts_db.get_malicious()
		index = 0
		for hist_pub in posts_db.get_hist_publications():
			hyp_is_mal_gt = {}
			for user in hist_pub.keys():
				label = False
				if user in malicious:
					label = True
				if not user in hyp_is_mal_gt_full.keys():
					hyp_is_mal_gt[user] = label
					if label:
						clone_time_log = copy.deepcopy(time_log)
						clone_time_log['start'] = index
						hyp_is_mal_time[user] = clone_time_log
				hyp_is_mal_gt_full[user] = label
			orig_hyp_is_mal_gt_time.append(hyp_is_mal_gt)
			index += 1


		orig_hyp_botnet_member_gt_time = []
		hyp_botnet_member_gt_full = {}
		hyp_botnet_member_time = {}
		detection_times.append({'name': 'hyp_botnet_member_time', 'value': hyp_botnet_member_time})
		node_index = 0
		total_users = posts_db.get_nodes_id()
		for node_index in range(len(total_users)):
			for other_node_index in range(len(total_users)):
				hyp_botnet_member_gt_full['(' + str(total_users[node_index]) + ',' + str(total_users[other_node_index]) + ')'] = False
		
		botnets = posts_db.get_members_in_botnets()

		index = 0
		for hist_pub in posts_db.get_hist_publications():
			hyp_botnet_member_gt = {}
			#users1 = copy.deepcopy(hist_pub.keys())
			#users2 = copy.deepcopy(hist_pub.keys())
			users = list(hist_pub.keys())
			for node_index in range(len(users)):
				for other_node_index in range(len(users)):
					label = False
					for botnet in botnets:
						if users[node_index] in copy.deepcopy(botnet) and users[other_node_index] in copy.deepcopy(botnet):
							label = True
							break
					found = False
					for time_gt in orig_hyp_botnet_member_gt_time:
						if '(' + str(users[node_index]) + ',' + str(users[other_node_index]) + ')' in time_gt.keys():
							found = True
							break
					if not found:
						hyp_botnet_member_gt['(' + str(users[node_index]) + ',' + str(users[other_node_index]) + ')'] = label
						if label:
							clone_time_log = copy.deepcopy(time_log)
							clone_time_log['start'] = index
							hyp_botnet_member_time['(' + str(users[node_index]) + ',' + str(users[other_node_index]) + ')'] = clone_time_log
					hyp_botnet_member_gt_full['(' + str(users[node_index]) + ',' + str(users[other_node_index]) + ')'] = label
			orig_hyp_botnet_member_gt_time.append(hyp_botnet_member_gt)
			index += 1


		earlyPoster = EarlyPoster(posts_db)
		closer = Closer(posts_db)
		news_category = NewsCategory(posts_db)

		atoms = []
		facts = []
		kbs = []
		gt_fn_atoms = []

		kbs.append(NetDERKB(ont_data = atoms, net_db = NetDB(graph, facts), netder_tgds = tgds1, netder_egds = egds, netdiff_lrules = local_rules, netdiff_grules = global_rules))
		kbs.append(NetDERKB(ont_data = atoms, net_db = NetDB(graph, facts), netder_tgds = tgds2, netder_egds = egds, netdiff_lrules = local_rules, netdiff_grules = global_rules))
		kbs.append(NetDERKB(ont_data = [], net_db = NetDB(graph, facts), netder_tgds = tgds3, netder_egds = egds, netdiff_lrules = local_rules, netdiff_grules = global_rules))
		for i in range(len(kbs)):
			gt_fn_atoms.append([])
			for j in range(time_sim):
				gt_fn_atoms[i].append([])
			
		for i in range(len(orig_news_ground_truth_full)):
			for key in orig_news_ground_truth_full[i].keys():
				if orig_news_ground_truth_full[i][key]:
					gt_fn_atoms[len(gt_fn_atoms) - 1][i].append(Atom('hyp_fakenews', [Constant(str(key))]))


		for kb_index in range(len(kbs)):
			news_ground_truth_full = copy.deepcopy(orig_news_ground_truth_full)
			news1_ground_truth_full = copy.deepcopy(orig_news1_ground_truth_full)
			news2_ground_truth_full = copy.deepcopy(orig_news2_ground_truth_full)
			hyp_is_resp_gt_time = copy.deepcopy(orig_hyp_is_resp_gt_time)
			hyp_is_mal_gt_time = copy.deepcopy(orig_hyp_is_mal_gt_time)
			hyp_botnet_member_gt_time = copy.deepcopy(orig_hyp_botnet_member_gt_time)
			kb = kbs[kb_index]
			chase = NetDERChase(kb, tmax)
			answers_hyp_fakenews = []
			answers_hyp_fakenews1 = [] 
			answers_hyp_fakenews2 = []
			answers_hyp_is_resp = []
			answers_hyp_malicious = []
			answers_hyp_member = []
			reduced_result_eval = {}
			for item in ['fnA', 'fnB', 'fnC', 'resp', 'mal', 'memb']:
				reduced_result_eval[item] = []

			for time in range(time_sim):
				print('time:', time)
				answers_hyp_fakenews.append([])
				answers_hyp_fakenews1.append([])
				answers_hyp_fakenews2.append([])
				answers_hyp_is_resp.append([])
				answers_hyp_malicious.append([])
				answers_hyp_member.append([])
				result_eval["time_sim"] = time
				

				#atoms = atoms + ont_db[time]
				#atoms = atoms + earlyPoster.get_atoms()

				atoms = gt_fn_atoms[kb_index][time] + ont_db[time] + earlyPoster.get_atoms(time) + closer.get_atoms(time) + news_category.get_atoms(time)
				#atoms = ont_db[time] + earlyPoster.get_atoms()
				print('len(new_atoms):', len(atoms))

				print('antes de remover pre_hyp_fakenews len(ont_db):', kb.get_ont_db().get_size())

				#kb.remove_atoms_from_pred('pre_hyp_fakenews')
				print('despues de remover pre_hyp_fakenews len(ont_db):', kb.get_ont_db().get_size())
				kb.add_ont_knowledge(atoms)

				print('despues de agregar new atoms len(ont_db):', kb.get_ont_db().get_size())
				#facts = facts + net_db[time]
				facts = net_db[time]
				kb_net_db = kb.get_net_db()
				kb_net_db.set_facts(facts)
				#kb = NetDERKB(ont_data = atoms, net_db = NetDB(graph, facts), netder_tgds = tgds, netder_egds = egds, netdiff_lrules = local_rules, netdiff_grules = global_rules)
				chase = NetDERChase(kb, tmax)

				inicio_q1 = datetime.now()
				answers = chase.answer_query(query1, 1)
				fin_q1 = datetime.now()

				
				if not answers is None:
					print('len answers:', len(answers))
					for answer in answers:
						contador = 0
						if 'X' in answer.keys():
							value = answer['X'].getValue()
							found = False
							for t in range(time):
								if value in answers_hyp_fakenews[t]:
									found = True
									break
							if not found:
								answers_hyp_fakenews[time].append(value)
								if not value in news_ground_truth_full[time].keys():
									news_ground_truth_full[time][value] = news_dataset_ground_truth[value]
								

						if 'Y' in answer.keys() and 'Z' in answer.keys():
							value = '(' + str(answer['Y'].getValue()) + ',' + str(answer['Z'].getValue()) + ')'
							found = False
							for t in range(time):
								if value in answers_hyp_is_resp[t]:
									found = True
									break
							if not found:
								answers_hyp_is_resp[time].append(value)
								if value in hyp_is_resp_time.keys():
									hyp_is_resp_time[value]['end'] = time
				
								if not value in hyp_is_resp_gt_time[time].keys():
									hyp_is_resp_gt_time[time][value] = hyp_is_resp_gt_full[value]

						if 'M' in answer.keys():
							value = str(answer['M'].getValue())
							found = False
							for t in range(time):
								if value in answers_hyp_malicious[t]:
									found = True
									break
							if not found:
								answers_hyp_malicious[time].append(value)
								if value in hyp_is_mal_time.keys():
									hyp_is_mal_time[value]['end'] = time
								if not value in hyp_is_mal_gt_time[time].keys():
									hyp_is_mal_gt_time[time][value] = hyp_is_mal_gt_full[value]
						
						if 'UID1' in answer.keys() and 'UID2' in answer.keys():
							value = '(' + str(answer['UID1'].getValue()) + ',' + str(answer['UID2'].getValue()) + ')'
							found = False
							for t in range(time):
								if value in answers_hyp_member[t]:
									found = True
									break
							if not found:
								if value in hyp_botnet_member_time.keys():
									hyp_botnet_member_time[value]['end'] = time
								answers_hyp_member[time].append(value)
								if not value in hyp_botnet_member_gt_time[time].keys():
									hyp_botnet_member_gt_time[time][value] = hyp_botnet_member_gt_full[value]


				print('len(answers_hyp_fakenews)')
				print(len(answers_hyp_fakenews[time]))
				print('len pre_hyp_fakenews1')
				for pre_hyp_fn in kb.get_ont_db().get_atoms_from_pred('pre_hyp_fakenews'):
					value = pre_hyp_fn.get_terms()[0].getValue()
					found = False
					for t in range(time):
						if value in answers_hyp_fakenews1[t]:
							found = True
							break
					if not found:
						answers_hyp_fakenews1[time].append(value)
						if not value in news1_ground_truth_full[time].keys():
							news1_ground_truth_full[time][value] = news_dataset_ground_truth[value]
						'''
						if time < time_sim:
							for t in range(time + 1, time_sim):
								news1_ground_truth_full[t].pop(value)'''
				
				print(len(answers_hyp_fakenews1[time]))

				print('len pre_hyp_fakenews2')
				for pre_hyp_fn in kb.get_ont_db().get_atoms_from_pred('pre_hyp_fakenews2'):
					value = pre_hyp_fn.get_terms()[0].getValue()
					found = False
					for t in range(time):
						if value in answers_hyp_fakenews2[t]:
							found = True
							break
					if not found:
						answers_hyp_fakenews2[time].append(value)
						if not value in news2_ground_truth_full[time].keys():
							news2_ground_truth_full[time][value] = news_dataset_ground_truth[value]
				
				print(len(answers_hyp_fakenews2[time]))

				result_eval["fnA"] = len(answers_hyp_fakenews[time])
				print('len(answers_hyp_is_resp)')
				print(len(answers_hyp_is_resp[time]))
				result_eval["resp"] = len(answers_hyp_is_resp[time])
				print('len(answers_hyp_malicious)')
				print(len(answers_hyp_malicious[time]))
				result_eval["mal"] = len(answers_hyp_malicious[time])
				print('len(answers_hyp_member)')
				print(len(answers_hyp_member[time]))
				result_eval["memb"] = len(answers_hyp_member[time])

				print('len(news_ground_truth_full[time])', len(news_ground_truth_full[time]))
				print('answers_hyp_fakenews', len(answers_hyp_fakenews[time]))
				evaluator1 = Evaluator(news_ground_truth_full[time], answers_hyp_fakenews[time])
				result_eval1 = evaluator1.evaluate()
				result_eval["fnA_prec"] = None
				result_eval["fnA_rec"] = None
				'''
				if not result_eval1["precision"] is None:
					reduced_result_eval["fnA_prec"]['total_value'] += result_eval1["precision"]
				else:
					reduced_result_eval["fnA_prec"]['total_samples'] -= 1
				result_eval["fnA_rec"] = result_eval1["recall"]
				if not result_eval1["recall"] is None:
					reduced_result_eval["fnA_rec"]['total_value'] += result_eval1["recall"]
				else:
					reduced_result_eval["fnA_rec"]['total_samples'] -= 1
				if not result_eval1["f1"] is None:
					reduced_result_eval["fnA_f1"]['total_value'] += result_eval1["f1"]
				else:
					reduced_result_eval["fnA_f1"]['total_samples'] -= 1'''
				reduced_result_eval["fnA"].append(result_eval1)
				result_eval["fnA_tp"] = result_eval1["tp"]
				result_eval["fnA_fp"] = result_eval1["fp"]
				result_eval["fnA_tn"] = result_eval1["tn"]
				result_eval["fnA_fn"] = result_eval1["fn"]
				evaluator2 = Evaluator(hyp_is_resp_gt_time[time], answers_hyp_is_resp[time])
				result_eval2 = evaluator2.evaluate()
				result_eval["resp_prec"] = None
				result_eval["resp_rec"] = None
				'''
				if not result_eval2["precision"] is None:
					reduced_result_eval["resp_prec"]['total_value'] += result_eval2["precision"]
				else:
					reduced_result_eval["resp_prec"]['total_samples'] -= 1
				result_eval["resp_rec"] = result_eval2["recall"]
				if not result_eval2["recall"] is None:
					reduced_result_eval["resp_rec"]['total_value'] += result_eval2["recall"]
				else:
					reduced_result_eval["resp_rec"]['total_samples'] -= 1
				if not result_eval2["f1"] is None:
					reduced_result_eval["resp_f1"]['total_value'] += result_eval2["f1"]
				else:
					reduced_result_eval["resp_f1"]['total_samples'] -= 1'''
				reduced_result_eval["resp"].append(result_eval2)
				result_eval["resp_tp"] = result_eval2["tp"]
				result_eval["resp_fp"] = result_eval2["fp"]
				result_eval["resp_tn"] = result_eval2["tn"]
				result_eval["resp_fn"] = result_eval2["fn"]
				evaluator3 = Evaluator(hyp_is_mal_gt_time[time], answers_hyp_malicious[time])
				result_eval3 = evaluator3.evaluate()
				result_eval["mal_prec"] = None
				result_eval["mal_rec"] = None
				'''
				if not result_eval3["precision"] is None:
					reduced_result_eval["mal_prec"]['total_value'] += result_eval3["precision"]
				else:
					reduced_result_eval["mal_prec"]['total_samples'] -= 1
				result_eval["mal_rec"] = result_eval3["recall"]
				if not result_eval3["recall"] is None:
					reduced_result_eval["mal_rec"]['total_value'] += result_eval3["recall"]
				else:
					reduced_result_eval["mal_rec"]['total_samples'] -= 1
				if not result_eval3["f1"] is None:
					reduced_result_eval["mal_f1"]['total_value'] += result_eval3["f1"]
				else:
					reduced_result_eval["mal_f1"]['total_samples'] -= 1'''
				reduced_result_eval["mal"].append(result_eval3)
				result_eval["mal_tp"] = result_eval3["tp"]
				result_eval["mal_fp"] = result_eval3["fp"]
				result_eval["mal_tn"] = result_eval3["tn"]
				result_eval["mal_fn"] = result_eval3["fn"]
				evaluator4 = Evaluator(hyp_botnet_member_gt_time[time], answers_hyp_member[time])
				result_eval4 = evaluator4.evaluate()
				result_eval["memb_prec"] = None
				result_eval["memb_rec"] = None
				'''
				if not result_eval4["precision"] is None:
					reduced_result_eval["memb_prec"]['total_value'] += result_eval4["precision"]
				else:
					reduced_result_eval["memb_prec"]['total_samples'] -= 1
				result_eval["memb_rec"] = result_eval4["recall"]
				if not result_eval4["recall"] is None:
					reduced_result_eval["memb_rec"]['total_value'] += result_eval4["recall"]
				else:
					reduced_result_eval["memb_rec"]['total_samples'] -= 1
				if not result_eval4["f1"] is None:
					reduced_result_eval["memb_f1"]['total_value'] += result_eval4["f1"]
				else:
					reduced_result_eval["memb_f1"]['total_samples'] -= 1'''
				reduced_result_eval["memb"].append(result_eval4)
				result_eval["memb_tp"] = result_eval4["tp"]
				result_eval["memb_fp"] = result_eval4["fp"]
				result_eval["memb_tn"] = result_eval4["tn"]
				result_eval["memb_fn"] = result_eval4["fn"]
				evaluator5 = Evaluator(news1_ground_truth_full[time], answers_hyp_fakenews1[time])
				result_eval5 = evaluator5.evaluate()
				result_eval["fnB_prec"] = None
				result_eval["fnB_rec"] = None
				'''
				if not result_eval5["precision"] is None:
					reduced_result_eval["fnB_prec"]['total_value'] += result_eval5["precision"]
				else:
					reduced_result_eval["fnB_prec"]['total_samples'] -= 1
				result_eval["fnB_rec"] = result_eval5["recall"]
				if not result_eval5["recall"] is None:
					reduced_result_eval["fnB_rec"]['total_value'] += result_eval5["recall"]
				else:
					reduced_result_eval["fnB_rec"]['total_samples'] -= 1
				if not result_eval5["f1"] is None:
					reduced_result_eval["fnB_f1"]['total_value'] += result_eval5["f1"]
				else:
					reduced_result_eval["fnB_f1"]['total_samples'] -= 1'''
				reduced_result_eval["fnB"].append(result_eval5)
				result_eval["fnB_tp"] = result_eval5["tp"]
				result_eval["fnB_fp"] = result_eval5["fp"]
				result_eval["fnB_tn"] = result_eval5["tn"]
				result_eval["fnB_fn"] = result_eval5["fn"]
				evaluator6 = Evaluator(news2_ground_truth_full[time], answers_hyp_fakenews2[time])
				result_eval6 = evaluator6.evaluate()
				result_eval["fnC_prec"] = None
				result_eval["fnC_rec"] = None
				'''
				if not result_eval6["precision"] is None:
					reduced_result_eval["fnC_prec"]['total_value'] += result_eval6["precision"]
				else:
					reduced_result_eval["fnC_prec"]['total_samples'] -= 1
				result_eval["fnC_rec"] = result_eval6["recall"]
				if not result_eval6["recall"] is None:
					reduced_result_eval["fnC_rec"]['total_value'] += result_eval6["recall"]
				else:
					reduced_result_eval["fnC_rec"]['total_samples'] -= 1
				if not result_eval6["f1"] is None:
					reduced_result_eval["fnC_f1"]['total_value'] += result_eval6["f1"]
				else:
					reduced_result_eval["fnC_f1"]['total_samples'] -= 1'''
				reduced_result_eval["fnC"].append(result_eval6)
				result_eval["fnC_tp"] = result_eval6["tp"]
				result_eval["fnC_fp"] = result_eval6["fp"]
				result_eval["fnC_tn"] = result_eval6["tn"]
				result_eval["fnC_fn"] = result_eval6["fn"]

				print("Evaluacion hyp_fakenews:", result_eval1)
				print("Evaluacion pre_fake_news1:", result_eval5)
				print("Evaluacion pre_fake_news2:", result_eval6)
				print("Evaluacion hyp_is_resp:", result_eval2)
				print("Evaluacion hyp_is_malicious:", result_eval3)
				print("Evaluacion hyp_members:", result_eval4)

				print('Tiempo chase consulta 1:', fin_q1 - inicio_q1)

				result_eval["query_time"] = fin_q1 - inicio_q1

				'''
				with open('../result_netder_experiment.csv', 'a+', newline='') as csvfile:
					fieldnames = ["setting", "run", "query_time", "time_sim", "hyp_fakenews", "hyp_fn_precision", "hyp_fn_recall", "hyp_fn1_precision", "hyp_fn1_recall", "hyp_fn2_precision", "hyp_fn2_recall", "hyp_fakenews_tp", "hyp_fakenews_fp", "hyp_fakenews_tn", "hyp_fakenews_fn", "hyp_is_resp", "h_resp_precision", "h_resp_recall", "hyp_is_resp_tp", "hyp_is_resp_fp", "hyp_is_resp_tn", "hyp_is_resp_fn", "hyp_is_malicious", "h_mal_precision", "h_mal_recall", "hyp_is_malicious_tp", "hyp_is_malicious_fp", "hyp_is_malicious_tn", "hyp_is_malicious_fn", "hyp_members", "h_memb_precision", "h_memb_recall", "hyp_members_tp", "hyp_members_fp", "hyp_members_tn", "hyp_members_fn"]
					reader = csv.DictReader(csvfile)
					writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
					#writer.writeheader()
					writer.writerows(list(reader))
					writer.writerow(result_eval)'''

				if time == (time_sim - 1):
					for key in reduced_result_eval.keys():
						tp = 0
						fp = 0
						fn = 0
						prec = None
						rec = None
						f1 = None
						for evaluator in reduced_result_eval[key]:
							tp += evaluator['tp']
							fp += evaluator['fp']
							fn += evaluator['fn']
						if (fp + tp) != 0:
							prec = tp / (fp + tp)
							reduced_result_eval2[kb_index][str(key) + '_' + 'prec']['total_value'] += prec
							result_eval[str(key) + '_' + 'prec'] = prec
						else:
							reduced_result_eval2[kb_index][str(key) + '_' + 'prec']['total_samples'] -= 1

						if (fn + tp) != 0:
							rec = tp / (fn + tp)
							reduced_result_eval2[kb_index][str(key) + '_' + 'rec']['total_value'] += rec
							result_eval[str(key) + '_' + 'rec'] = rec
						else:
							reduced_result_eval2[kb_index][str(key) + '_' + 'rec']['total_samples'] -= 1				
						
						if not ((prec is None or rec is None) or (prec == 0 and rec == 0)):
							f1 = 2*(prec*rec)/(prec + rec)
							reduced_result_eval2[kb_index][str(key) + '_' + 'f1']['total_value'] += f1
						else:
							reduced_result_eval2[kb_index][str(key) + '_' + 'f1']['total_samples'] -= 1

				save_csv('../result_netder_experiment_prog'+ str(kb_index + 1)+'.csv', result_eval)
			

			
			for detection in detection_times:
				writepath = '../time_detection_results/' + detection['name'] + '_sett' + setting_values['setting'] + '_run'+ str(run + 1) + '_prog' + str(kb_index + 1) + '.json'
				with open(writepath, 'w') as outfile:
					json.dump(detection['value'], outfile)
				

			member_data = kb.get_data_from_pred('member')
			print('len(member_data)', len(member_data))

			print('Tiempo construccion DB:', fin_bdb - inicio_bdb)
			fin_setting = datetime.now()
			print('Tiempo setting nro', setting_values['setting'], 'run nro', run + 1,':', fin_setting - inicio_setting)
			setting_counter += 1
			gt = news_ground_truth_full[time_sim - 1]
			fn = 0
			rn = 0
			fn_cat_counter = {}
			rn_cat_counter = {}
			for category in fn_dataset.get_category_kinds():
				fn_cat_counter[category] = 0
				rn_cat_counter[category] = 0

			for key in gt.keys():
				category = fn_dataset.get_category(key)
				if gt[key] == True:
					fn_cat_counter[category] += 1
					fn += 1
				elif gt[key] == False:
					rn_cat_counter[category] += 1
					rn += 1
			print('setting', setting_values['setting'], 'run', run + 1)
			print('porcentaje fake news', fn / len(gt))
			print('porcentaje real news', rn / len(gt))
			print('cuenta por categoria en fn', fn_cat_counter)
			print('cuenta por categoria en rn', rn_cat_counter)

			

	rr_counter = 0
	for rr in reduced_result_eval2:
		for key in rr.keys():
			#time_sim_val = int(setting_values["time_sim"])
			#cant_run_val = int(setting_values["cant_run"])
			prev_value = rr[key]['total_value']
			total_samples = rr[key]['total_samples']
			if total_samples > 0:
				rr[key] = prev_value / total_samples
			else:
				rr[key] = None

		rr['setting'] = setting_values['setting']
		save_csv('../reduced_result_experiment_prog'+ str(rr_counter + 1)+'.csv', rr)
		rr_counter += 1

fin = datetime.now()
print('Tiempo total:',fin - inicio)
