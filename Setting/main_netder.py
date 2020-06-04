import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from datetime import datetime
import csv
import portion
import copy
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
	for run in range(int(setting_values["cant_run"])):
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


		#sacar esto, no va
		#for p in logic_database[0]:
		#	category = fn_dataset.get_category(p.get_terms()[1].getId())
		#	nlabel = NLocalLabel(category)
		#	facts.append(NetDiffFact(NetDiffNode(p.get_terms()[0]), nlabel, portion.closed(1, 1), 0, tmax))

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


		ont_head1 = Atom('hyp_fakenews', [Variable('FN')])
		ont_head2 = Atom('hyp_is_resp', [Variable('UID'), Variable('FN')])
		ont_head3 = Atom('hyp_malicious', [Variable('UID')])
		ont_head4 = [Atom('hyp_botnet', [Variable('B')]), Atom('member', [Variable('UID1'), Variable('B')]), Atom('member', [Variable('UID2'), Variable('B')])]

		global_conditions = []
		for glabel in category_glabels:
			#global_conditions.append((glabel, portion.closed(0.5, 1)))
			global_conditions.append((glabel, portion.closed(float(setting_values["trending_interval_lower"]), float(setting_values["trending_interval_upper"]))))

		tgds = []
		#news(FN, fake_level) ^ (fake_level > \theta_1) -> hyp_fakeNews(FN) : trending(FN)
		#pre_hyp_fakenews(FN) -> hyp_fakeNews(FN) : trending(FN)
		#pre_hyp_fakenews(FN) ^ news_category(FN, C)-> hyp_fakeNews(FN) : trending(C)
		tgd_counter = 0
		for gc in global_conditions:
			#tgds.append(NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom8], ont_head = [ont_head1], global_cond = [gc]))
			news_category_atom = Atom('news_category', [Variable('FN'), Constant(category_kinds[tgd_counter])])
			tgds.append(NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom8, news_category_atom], ont_head = [ont_head1], global_cond = [gc]))
			tgd_counter += 1

		#hyp_fakeNews(FN) ^ earlyPoster(UID, FN) ^ user(UID, N) -> hyp_is_resp(UID, FN)
		#hyp_fakeNews(FN) ^ earlyPoster(UID, FN) -> hyp_is_resp(UID, FN)

		tgd1 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [ont_head1, atom4], ont_head = [ont_head2])
		tgd_counter += 1

		#hyp_is_resp(UID, FN1) ^ hyp_is_resp(UID, FN2) ^ (FN1 != FN2) -> hyp_malicious(UID)

		tgd2 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom5, atom6, atom7], ont_head = [ont_head3])
		tgd_counter += 1

		#hyp_malicious(UID1) ^ hyp_malicious(UID2) ^ closer(UID1, UID2) ^ (V > \theta_2) ^ (UID1 != UID2) -> \exists B hyp_botnet(B) ^ member(UID1, B) ^ member(UID2, B)
		tgd3 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom9, atom10, atom11], ont_head = ont_head4)
		tgd_counter += 1

		tgd4 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom12], ont_head = [ont_head1])
		tgd_counter += 1

		tgds.append(tgd1)
		tgds.append(tgd2)
		tgds.append(tgd3)
		tgds.append(tgd4)
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

		news_ground_truth_full = []
		index = 0
		for posts_in_time in posts_db.get_news():
			news_ground_truth = {}
			for news in posts_in_time:
				news_ground_truth[news] = news_dataset_ground_truth[news]
			if index > 0:
				news_ground_truth_full.append(copy.deepcopy(news_ground_truth_full[index - 1]))
				news_ground_truth_full[index].update(news_ground_truth)
			else: 
				news_ground_truth_full.append(news_ground_truth)

			index += 1

		index = 0
		hyp_is_resp_gt_full = []
		for hist_pub in posts_db.get_hist_publications():
			hyp_is_resp_gt = {}
			if (index - 1) >= 0:
				hyp_is_resp_gt = hyp_is_resp_gt_full[index - 1]
			for node in posts_db.get_nodes_id():
				for key in hist_pub.keys():
					hyp_is_resp_gt['(' + str(node) + ',' +str(hist_pub[key]) + ')'] = False

			hyp_is_resp_gt_full.append(hyp_is_resp_gt)
			index += 1

		index = 0
		for hist_pub in posts_db.get_hist_publications():
			hyp_is_resp_gt = {}
			for node in posts_db.get_malicious():
				if (node in hist_pub.keys()) and (news_dataset_ground_truth[hist_pub[node]]):
					hyp_is_resp_gt['(' + str(node) + ',' + str(hist_pub[node]) + ')'] = True

			if index - 1 >= 0:
				hyp_is_resp_gt_full[index].update(hyp_is_resp_gt_full[index - 1])

			hyp_is_resp_gt_full[index].update(hyp_is_resp_gt)
			index += 1

		hyp_is_mal_gt_full = {}

		for node_id in posts_db.get_nodes_id():
			hyp_is_mal_gt_full[node_id] = False

		for mal in posts_db.get_malicious():
			hyp_is_mal_gt_full[mal] = True

		hyp_botnet_member_gt_full = {}
		node_index = 0
		users = posts_db.get_nodes_id()
		for node_index in range(len(users)):
			#for other_node_index in range(node_index + 1, len(users)):
			for other_node_index in range(len(users)):
				hyp_botnet_member_gt_full['(' + str(users[node_index]) + ',' + str(users[other_node_index]) + ')'] = False

		for botnet in posts_db.get_members_in_botnets():
			for user in botnet:
				for other_user in copy.deepcopy(botnet):
					hyp_botnet_member_gt_full['(' + str(user) + ',' + str(other_user) + ')'] = True

		earlyPoster = EarlyPoster(posts_db)
		closer = Closer(posts_db)
		news_category = NewsCategory(posts_db)

		atoms = []
		facts = []

		kb = NetDERKB(ont_data = atoms, net_db = NetDB(graph, facts), netder_tgds = tgds, netder_egds = egds, netdiff_lrules = local_rules, netdiff_grules = global_rules)
		chase = NetDERChase(kb, tmax)

		for time in range(time_sim):
			print('time:', time)
			result_eval["time_sim"] = time
			

			#atoms = atoms + ont_db[time]
			#atoms = atoms + earlyPoster.get_atoms()
			
			atoms = ont_db[time] + earlyPoster.get_atoms() + closer.get_atoms() + news_category.get_atoms()
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
			#answers = []
			answers = chase.answer_query(query1, 1)
			fin_q1 = datetime.now()

			answers_hyp_fakenews = []
			answers_hyp_fakenews1 = []
			answers_hyp_fakenews2 = []
			answers_hyp_is_resp = []
			answers_hyp_malicious = []
			answers_hyp_member = []
			if not answers is None:
				print('len answers:', len(answers))
				for answer in answers:
					contador = 0
					if 'X' in answer.keys():
						value = answer['X'].getValue()
						answers_hyp_fakenews.append(value)

					if 'Y' in answer.keys() and 'Z' in answer.keys():
						answers_hyp_is_resp.append('(' + str(answer['Y'].getValue()) + ',' + str(answer['Z'].getValue()) + ')')

					if 'M' in answer.keys():
						answers_hyp_malicious.append(str(answer['M'].getValue()))
					
					if 'UID1' in answer.keys() and 'UID2' in answer.keys():
						value = '(' + str(answer['UID1'].getValue()) + ',' + str(answer['UID2'].getValue()) + ')'
						answers_hyp_member.append(value)


			print('len(answers_hyp_fakenews)')
			print(len(answers_hyp_fakenews))
			print('len pre_hyp_fakenews1')
			for pre_hyp_fn in kb.get_ont_db().get_atoms_from_pred('pre_hyp_fakenews'):
				value = pre_hyp_fn.get_terms()[0].getValue()
				answers_hyp_fakenews1.append(value)
			
			print(len(answers_hyp_fakenews1))

			print('len pre_hyp_fakenews2')
			for pre_hyp_fn in kb.get_ont_db().get_atoms_from_pred('pre_hyp_fakenews2'):
				value = pre_hyp_fn.get_terms()[0].getValue()
				answers_hyp_fakenews2.append(value)
			
			print(len(answers_hyp_fakenews2))

			result_eval["hyp_fakenews"] = len(answers_hyp_fakenews)
			print('len(answers_hyp_is_resp)')
			print(len(answers_hyp_is_resp))
			result_eval["hyp_is_resp"] = len(answers_hyp_is_resp)
			print('len(answers_hyp_malicious)')
			print(len(answers_hyp_malicious))
			result_eval["hyp_is_malicious"] = len(answers_hyp_malicious)
			print('len(answers_hyp_member)')
			print(len(answers_hyp_member))
			result_eval["hyp_members"] = len(answers_hyp_member)

			print('len(news_ground_truth_full[time])', len(news_ground_truth_full[time]))
			print('answers_hyp_fakenews', len(answers_hyp_fakenews))
			evaluator1 = Evaluator(news_ground_truth_full[time], answers_hyp_fakenews)
			result_eval1 = evaluator1.evaluate()
			result_eval["hyp_fn_precision"] = result_eval1["precision"]
			result_eval["hyp_fn_recall"] = result_eval1["recall"]
			result_eval["hyp_fakenews_tp"] = result_eval1["tp"]
			result_eval["hyp_fakenews_fp"] = result_eval1["fp"]
			result_eval["hyp_fakenews_tn"] = result_eval1["tn"]
			result_eval["hyp_fakenews_fn"] = result_eval1["fn"]
			evaluator2 = Evaluator(hyp_is_resp_gt_full[time], answers_hyp_is_resp)
			result_eval2 = evaluator2.evaluate()
			result_eval["h_resp_precision"] = result_eval2["precision"]
			result_eval["h_resp_recall"] = result_eval2["recall"]
			result_eval["hyp_is_resp_tp"] = result_eval2["tp"]
			result_eval["hyp_is_resp_fp"] = result_eval2["fp"]
			result_eval["hyp_is_resp_tn"] = result_eval2["tn"]
			result_eval["hyp_is_resp_fn"] = result_eval2["fn"]
			evaluator3 = Evaluator(hyp_is_mal_gt_full, answers_hyp_malicious)
			result_eval3 = evaluator3.evaluate()
			result_eval["h_mal_precision"] = result_eval3["precision"]
			result_eval["h_mal_recall"] = result_eval3["recall"]
			result_eval["hyp_is_malicious_tp"] = result_eval3["tp"]
			result_eval["hyp_is_malicious_fp"] = result_eval3["fp"]
			result_eval["hyp_is_malicious_tn"] = result_eval3["tn"]
			result_eval["hyp_is_malicious_fn"] = result_eval3["fn"]
			evaluator4 = Evaluator(hyp_botnet_member_gt_full, answers_hyp_member)
			result_eval4 = evaluator4.evaluate()
			result_eval["h_memb_precision"] = result_eval4["precision"]
			result_eval["h_memb_recall"] = result_eval4["recall"]
			result_eval["hyp_members_tp"] = result_eval4["tp"]
			result_eval["hyp_members_fp"] = result_eval4["fp"]
			result_eval["hyp_members_tn"] = result_eval4["tn"]
			result_eval["hyp_members_fn"] = result_eval4["fn"]
			evaluator5 = Evaluator(news_ground_truth_full[time], answers_hyp_fakenews1)
			result_eval5 = evaluator5.evaluate()
			result_eval["hyp_fn1_precision"] = result_eval5["precision"]
			result_eval["hyp_fn1_recall"] = result_eval5["recall"]
			evaluator6 = Evaluator(news_ground_truth_full[time], answers_hyp_fakenews2)
			result_eval6 = evaluator6.evaluate()
			result_eval["hyp_fn2_precision"] = result_eval6["precision"]
			result_eval["hyp_fn2_recall"] = result_eval6["recall"]

			print("Evaluacion hyp_fakenews:", result_eval1)
			print("Evaluacion pre_fake_news1:", result_eval5)
			print("Evaluacion pre_fake_news2:", result_eval6)
			print("Evaluacion hyp_is_resp:", result_eval2)
			print("Evaluacion hyp_is_malicious:", result_eval3)
			print("Evaluacion hyp_members:", result_eval4)

			print('Tiempo chase consulta 1:', fin_q1 - inicio_q1)

			result_eval["query_time"] = fin_q1 - inicio_q1

			with open('../result_netder_experiment.csv', 'a+', newline='') as csvfile:
				fieldnames = ["setting", "run", "query_time", "time_sim", "hyp_fakenews", "hyp_fn_precision", "hyp_fn_recall", "hyp_fn1_precision", "hyp_fn1_recall", "hyp_fn2_precision", "hyp_fn2_recall", "hyp_fakenews_tp", "hyp_fakenews_fp", "hyp_fakenews_tn", "hyp_fakenews_fn", "hyp_is_resp", "h_resp_precision", "h_resp_recall", "hyp_is_resp_tp", "hyp_is_resp_fp", "hyp_is_resp_tn", "hyp_is_resp_fn", "hyp_is_malicious", "h_mal_precision", "h_mal_recall", "hyp_is_malicious_tp", "hyp_is_malicious_fp", "hyp_is_malicious_tn", "hyp_is_malicious_fn", "hyp_members", "h_memb_precision", "h_memb_recall", "hyp_members_tp", "hyp_members_fp", "hyp_members_tn", "hyp_members_fn"]
				reader = csv.DictReader(csvfile)
				writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
				#writer.writeheader()
				writer.writerows(list(reader))
				writer.writerow(result_eval)
			


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

fin = datetime.now()
print('Tiempo total:',fin - inicio)