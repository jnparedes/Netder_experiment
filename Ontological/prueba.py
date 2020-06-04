import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Variable import Variable
from Constant import Constant
from Atom import Atom
from NetDERKB import NetDERKB
from NetDERChase import NetDERChase
from NetDERTGD import NetDERTGD
from NetDEREGD import NetDEREGD
from NetDERQuery import NetDERQuery
from NetCompTarget import NetCompTarget
from NetDB import NetDB
from Diffusion_Process.NetDiffFact import NetDiffFact
from Diffusion_Process.NetDiffGraph import NetDiffGraph
from Diffusion_Process.NetDiffNode import NetDiffNode
from Diffusion_Process.NetDiffEdge import NetDiffEdge
from Diffusion_Process.NLocalLabel import NLocalLabel
from Diffusion_Process.GlobalLabel import GlobalLabel
import copy
import portion

tmax = 1
nodes = [NetDiffNode('0'), NetDiffNode('1'), NetDiffNode('2'), NetDiffNode('3')]
edges = [NetDiffEdge('0', '1'), NetDiffEdge('2', '1'), NetDiffEdge('2', '3')]
red = NLocalLabel('red')
green = GlobalLabel('green')
nllabels = [red]
glabels = [green]

nodes[0].setLabels(nllabels)

graph = NetDiffGraph('graph', nodes, edges)
graph.setLabels(glabels)

facts = [NetDiffFact(nodes[0], red, portion.closed(0.5, 1), 0, tmax), NetDiffFact(graph, green, portion.closed(0.5, 1), 0, tmax)]

atoms = [Atom('padre', [Constant('a'), Constant('b')]), Atom('padre', [Constant('b'), Constant('c')])]

atom2 = Atom('padre', [Variable('X'), Variable('Y')])

atom3 = Atom('padre', [Variable('X'), Variable('Z')])

#Network Component Targets
nct1 = NetCompTarget(Atom('node', [Variable('T')]), red, portion.closed(0.5, 1))
nct2 = NetCompTarget(Atom('node', [Variable('S')]), red, portion.closed(0.5, 1))
nct3 = NetCompTarget(Atom('node', [Variable('S')]))

ont_head1 = Atom('abuelo', [Variable('X'), Variable('A')])
ont_head2 = Atom('tio', [Variable('X'), Variable('A')])
global_cond1 = (green, portion.closed(0.5, 1))

tgd = NetDERTGD(ont_body = [atom2, atom3], net_body = [nct1], ont_head = [ont_head1, ont_head2], net_head= [nct2],global_cond = [global_cond1])

egd1 = NetDEREGD(ont_body = [Atom('abuelo', [Variable('X'), Variable('Y')]), Atom('tio', [Variable('X'), Variable('Y')])], head=(Variable('X'), Variable('Y')))
egd2 = NetDEREGD(net_body = [nct2], head = (Variable('S'), Constant('0')))

kb = NetDERKB(ont_data = atoms, net_db = NetDB(graph, facts), netder_tgds=[tgd], netder_egds=[egd1, egd2])
chase = NetDERChase(kb)
query = NetDERQuery(exist_var = [], ont_cond = [Atom('abuelo', [Variable('X'), Variable('Y')]), Atom('tio', [Variable('A'), Variable('B')])], time = (0,1))

answers = None
answers = chase.answer_query(query, 1)

if answers is None:
	print('Respuesta: NO')
elif(len(answers) == 0):
	print('Respuesta: YES')
else:
	n = 0
	for answer in answers:
		n = n + 1
		print('Answer nro: ' + str(n))
		for key in answer.keys():
			print(key)
			print(str(answer[key]))

for comp in kb.get_net_diff_graph().get_components():
	print(str(comp))

print(chase.applyStepEGDChase(egd2, (0,1)))

'''
new_atoms = chase.applyStepTGDChase(tgd)

kb.add_atoms(new_atoms)

succes = chase.applyStepEGDChase(egd)

for atom in new_atoms:
	print(str(atom))

print(len(new_atoms))
print(succes)

for atom in kb.get_ont_data():
	print(str(atom))

'''