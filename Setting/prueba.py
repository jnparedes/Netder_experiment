import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from datetime import datetime
import csv
import portion
import copy
import random
from FakeNewsData.AugmentedDatasetCSVLiar import AugmentedDatasetCSVLiar
from FakeNewsData.DatasetCSVLiar import DatasetCSVLiar
from FakeNewsData.AugmentedDatasetTextFilesCelebrity import AugmentedDatasetTextFilesCelebrity
from AFPostDatabase import AFPostDatabase
from EarlyPoster import EarlyPoster
from Closer import Closer
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
from Ontological.Null import Null
from Ontological.NetCompTarget import NetCompTarget



'''
inicio = datetime.now()

tmax = 2
time_sim = 15
fk_threshold = 0.3

nodes = [NetDiffNode('0'), NetDiffNode('1'), NetDiffNode('2'), NetDiffNode('3')]
edges = [NetDiffEdge('0', '1'), NetDiffEdge('0', '2'), NetDiffEdge('0', '3'), NetDiffEdge('2', '3')]

graph = NetDiffGraph('graph', nodes, edges)
facts = []
null = Null()
atoms = [Atom('padre', [Constant('a'), null]), Atom('padre', [Constant('b'), null])]

kb = NetDERKB(ont_data = atoms, net_db = NetDB(graph, facts), netder_tgds = [], netder_egds = [], netdiff_lrules = [], netdiff_grules = [])

query1 = NetDERQuery(exist_var = [Variable('B')], ont_cond = [Atom('padre', [Variable('X'), Variable('B')]), Atom('padre', [Variable('Y'), Variable('B')]), Distinct(Variable('X'), Variable('Y'))], time = (2, 2))

chase = NetDERChase(kb, tmax)


#answers = chase.answer_query(query1, 1)

print('len(answers)', len(answers))
for ans in answers:
	for key in ans.keys():
		print('clave', key, 'valor', ans[key])

candidates = chase._get_candidate_atoms(query1)
print('len(candidates)', len(candidates))
q_mapping_list = chase._get_atoms_mapping(query1.get_ont_body(), candidates)

index = 0
print('otra prueba len(q_mapping_list)', len(q_mapping_list))
for possibility in q_mapping_list:
	print('possibility', index)
	aux_result_mapping = {}
	for mapping in possibility:
		for key in mapping.keys():
			#pass
			print('clave', key, 'valor', mapping[key])
	index += 1

'''
'''
def remove_id_posts(csv_file, id_posts):
	data = list()

	with open(csv_file, 'r',  newline='', encoding='utf-8') as readFile:
		reader = csv.reader(readFile, delimiter = '\t')
		counter = 0
		for row in reader:
			if not row[0] in id_posts:
				data.append(row)
			counter += 1

	with open(csv_file, 'w',  newline='', encoding='utf-8') as writeFile:
		writer = csv.writer(writeFile, delimiter = '\t')
		writer.writerows(data)

	return data

def get_rn(gt, id_posts):
	result = []
	for id_post in id_posts:
		if not gt[id_post]:
			result.append(id_post)

	return result

predicitions = PredictionsFakeNewsRob('hyp_fakenews', '../FakeNewsData/results/res_Liar.json', 0.2)
dataset = DatasetCSVLiar()
gt = dataset.get_ground_truth()
fn_goal_prop = 0.95
rn_goal_prop = 0.05
fn = 0
fn_tresh = 0 
rn = 0
rn_tresh = 0 
fn_cat_counter = {}
rn_cat_counter = {}
threshold = 0.5
news_thres = predicitions.get_id_posts(gt.keys(), threshold)
for category in dataset.get_category_kinds():
	fn_cat_counter[category] = 0
	rn_cat_counter[category] = 0

for key in gt.keys():
	category = dataset.get_category(key)
	if gt[key] == True:
		fn_cat_counter[category] += 1
		fn += 1
		if key in news_thres:
			fn_tresh += 1
	elif gt[key] == False:
		rn_cat_counter[category] += 1
		rn += 1
		if key in news_thres:
			rn_tresh += 1

real_news = get_rn(gt, news_thres)
cant_remove = int((1 - (((fn_tresh / len(news_thres)) * rn_goal_prop) / (fn_goal_prop * (rn_tresh / len(news_thres))))) * rn_tresh)
#remove_id_posts('../Datasets/Fake News/liar_dataset/train.tsv', real_news[:cant_remove])

print('len news_thres', len(news_thres))
print('porcentaje fake news', fn / len(gt))
print('proporcion de fn > threshold con respecto a todas las fn', fn_tresh / fn)
print('proporcion de fn > threshold con respecto a las news filtradas', fn_tresh / len(news_thres))
print('porcentaje real news', rn / len(gt))
print('proporcion de rn > threshold con respecto a todas las rn', rn_tresh / rn)
print('proporcion de rn > threshold con respecto a las news filtradas', rn_tresh / len(news_thres))
print('cuenta por categoria en fn', fn_cat_counter)
print('cuenta por categoria en rn', rn_cat_counter)
print('cantidad a remover', cant_remove)
print('len rn en news filtradas', len(real_news))
print('len rn en news filtradas', rn_tresh)

gt_keys = list(gt.keys())
gt1 = dataset.get_ground_truth()
print('len ground truth', len(gt))

id_posts = []
gt_map = {}
#cant_gt = len(gt)
cant_rn = 20
cant_fn = 80
random.shuffle(gt_keys)

for counter in range(cant_fn):
	index = random.randint(0, len(gt_keys) - 1)
	while gt[gt_keys[index]] == False or gt_keys[index] in id_posts:
		index = random.randint(0, len(gt_keys) - 1)
	
	id_posts.append(gt_keys[index])
	gt_map[gt_keys[index]] = gt[gt_keys[index]]


for counter in range(cant_fn, cant_rn):
	index = random.randint(0, len(gt_keys) - 1)
	while gt[gt_keys[index]] == True or gt_keys[index] in id_posts:
		index = random.randint(0, len(gt_keys) - 1)
	
	id_posts.append(gt_keys[index])
	gt_map[gt_keys[index]] = gt[gt_keys[index]]

atoms = []
atoms = predicitions.get_atoms(id_posts)

print('len atoms', len(atoms))
print('len id_posts', len(id_posts))

fake_news_predicitions = []
for atom in atoms:
	id_post = atom.get_terms()[0].getValue()
	fake_news_predicitions.append(id_post)

evaluator1 = Evaluator(gt_map, fake_news_predicitions)

print('evaluacion', evaluator1.evaluate())
'''


nodes = [NetDiffNode('0'), NetDiffNode('1'), NetDiffNode('2'), NetDiffNode('3')]
edges = [NetDiffEdge('0', '1'), NetDiffEdge('0', '2'), NetDiffEdge('0', '3'), NetDiffEdge('2', '3')]

graph = NetDiffGraph('graph', nodes, edges)

category_nlabels = []
category_glabels = []
category_kinds = ['A', 'B', 'C', 'D', 'E']
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

atom3 = Atom('user', [Variable('UID')])
atom4 = Atom('earlyPoster', [Variable('UID'), Variable('FN')])
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
atom17 = Atom('posted', [Variable('UID'), Variable('FN'), Variable('T')])
atom18 = Atom('hyp_malicious', [Variable('UID3')])
atom19 = Atom('closer', [Variable('UID1'), Variable('UID3')])
atom20 = Atom('posted', [Variable('UID1'), Variable('FN'), Variable('T')])
atom21 = Atom('posted', [Variable('UID2'), Variable('FN'), Variable('T')])
nct1 = NetCompTarget(atom16)


ont_head1 = Atom('hyp_fakenews', [Variable('FN')])
ont_head2 = Atom('hyp_is_resp', [Variable('UID'), Variable('FN')])
ont_head3 = Atom('hyp_malicious', [Variable('UID')])
#ont_head4 = [Atom('hyp_botnet', [Variable('B')]), Atom('member', [Variable('UID1'), Variable('B')]), Atom('member', [Variable('UID2'), Variable('B')]), Atom('member', [Variable('UID3'), Variable('B')])]
ont_head5 = [Atom('hyp_botnet', [Variable('B')]), Atom('member', [Variable('UID1'), Variable('B')]), Atom('member', [Variable('UID2'), Variable('B')])]

global_conditions = []
for glabel in category_glabels:
	global_conditions.append((glabel, portion.closed(0.1, 1)))
	#global_conditions.append((glabel, portion.closed(float(setting_values["trending_interval_lower"]), float(setting_values["trending_interval_upper"]))))

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
	tgds1.append(NetDERTGD(rule_id = tgd_counter, ont_body = [atom8, news_category_atom], ont_head = [ont_head1], global_cond = [gc]))
	tgd_counter += 1

#hyp_fakeNews(FN) ^ earlyPoster(UID, FN) ^ user(UID, N) -> hyp_is_resp(UID, FN)
#hyp_fakeNews(FN) ^ earlyPoster(UID, FN) -> hyp_is_resp(UID, FN)

tgd1 = NetDERTGD(rule_id = tgd_counter, ont_body = [ont_head1, atom4], ont_head = [ont_head2])
tgd_counter += 1

#(V1) hyp_is_resp(UID, FN1) ^ hyp_is_resp(UID, FN2) ^ (FN1 != FN2) -> hyp_malicious(UID)
#(V2) hyp_is_resp(UID, FN1) -> hyp_malicious(UID)

tgd2 = NetDERTGD(rule_id = tgd_counter, ont_body = [atom5, atom6, atom7], ont_head = [ont_head3])
#tgd2 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom5], ont_head = [ont_head3])
tgd_counter += 1

#hyp_malicious(UID1) ^ hyp_malicious(UID2) ^ closer(UID1, UID2) ^ (V > \theta_2) ^ (UID1 != UID2) -> \exists B hyp_botnet(B) ^ member(UID1, B) ^ member(UID2, B)
tgd3 = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom9, atom10, atom11], ont_head = ont_head5)
#tgd3 = NetDERTGD(rule_id = tgd_counter, ont_body = [atom13, atom14, atom15], ont_head = ont_head5)
#tgd3 = NetDERTGD(rule_id = tgd_counter, ont_body = [ont_head1, atom20, atom21, atom15], ont_head = ont_head5)
tgd_counter += 1

tgd4 = NetDERTGD(rule_id = tgd_counter, ont_body = [atom12], ont_head = [ont_head1])
tgd_counter += 1

tgd5 = NetDERTGD(rule_id = tgd_counter, ont_body = [atom9, atom10], net_body = [nct1], ont_head = ont_head5)
tgd_counter += 1

tgd6 = NetDERTGD(rule_id = tgd_counter, ont_body = [atom5], ont_head = [ont_head3])
tgd_counter += 1

tgd7 = NetDERTGD(rule_id = tgd_counter, ont_body = [ont_head1, atom17], ont_head = [ont_head2])
tgd_counter += 1

tgds1.append(tgd4)
tgds2 = copy.deepcopy(tgds1)
tgds1.append(tgd2)
tgds2.append(tgd6)
tgds1.append(tgd1)
tgds2.append(tgd7)
tgds1.append(tgd3)
tgds2.append(tgd5)
tgds3.append(tgd1)
tgds3.append(tgd2)
tgds3.append(tgd3)

egds = []
egd_counter = tgd_counter + 1
#hyp_botnet(B1) ^ hyp_botnet(B2) ^ member(UID, B1) ^ member(UID, B2) ->  B1 = B2
egd1 = NetDEREGD(rule_id = egd_counter, ont_body = [Atom('member', [Variable('UID'), Variable('B1')]), Atom('member', [Variable('UID'), Variable('B2')])], head = [Variable('B1'), Variable('B2')])

egds.append(egd1)



#glabel = GlobalLabel('gl')
#graph.setLabels([glabel])


#gc = (glabel, portion.closed(0.5, 1))

#atom8 = Atom('pre_hyp_fakenews', [Variable('FN')])
#news_category_atom = Atom('news_category', [Variable('FN'), Constant('A')])
#ont_head1 = Atom('hyp_fakenews', [Variable('FN')])

#tgds = []
#tgd = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom8, news_category_atom], ont_head = [ont_head1], global_cond = [gc])
#tgd_counter = 0 
#tgd = NetDERTGD(rule_id = 'tgd' + str(tgd_counter), ont_body = [atom8, news_category_atom], ont_head = [ont_head1], global_cond = [])
#tgds.append(tgd)

tmax = 2
facts = []
for n in nodes:
	facts.append(NetDiffFact(n, NLocalLabel('C'), portion.closed(1,1), 0, tmax))
atoms = [Atom('pre_hyp_fakenews', [Constant('fn1')]), Atom('news_category', [Constant('fn1'), Constant('C')]), Atom('pre_hyp_fakenews', [Constant('fn2')]), Atom('news_category', [Constant('fn2'), Constant('C')]), Atom('earlyPoster', [Constant('1'), Constant('fn1')]), Atom('earlyPoster', [Constant('1'), Constant('fn2')]), Atom('earlyPoster', [Constant('2'), Constant('fn3')]), Atom('earlyPoster', [Constant('2'), Constant('fn4')]), Atom('closer', [Constant('1'), Constant('2')]), Atom('pre_hyp_fakenews2', [Constant('fn3')]), Atom('pre_hyp_fakenews2', [Constant('fn4')])]

kb = NetDERKB(ont_data = atoms, net_db = NetDB(graph, facts), netder_tgds = tgds1, netder_egds = egds, netdiff_lrules = local_rules, netdiff_grules = global_rules)

chase = NetDERChase(kb, tmax)

query1 = NetDERQuery(exist_var = [Variable('B')], ont_cond = [Atom('hyp_fakenews', [Variable('X')]), Atom('hyp_is_resp', [Variable('Y'), Variable('Z')]), Atom('hyp_malicious', [Variable('M')]), Atom('member', [Variable('UID1'), Variable('B')])], time = (tmax, tmax))

answers = chase.answer_query(query1, 1)
for ans in answers:
	for key in ans.keys():
		print(key, ans[key])


