from NetDiffProgram import NetDiffProgram
from NetDiffFact import NetDiffFact
from NetDiffLocalRule import NetDiffLocalRule
from NetDiffGlobalRule import NetDiffGlobalRule
from Tipping import Tipping
from NetDiffGraph import NetDiffGraph
from NetDiffNode import NetDiffNode
from NetDiffEdge import NetDiffEdge
from Label import Label
from ELocalLabel import ELocalLabel
from NLocalLabel import NLocalLabel
from GlobalLabel import GlobalLabel
from Average import Average
from CFNetDiffFactRedLabels import CFNetDiffFactRedLabels
import portion

tmax = 1

nodes = [NetDiffNode('0'), NetDiffNode('1'), NetDiffNode('2'), NetDiffNode('3')]
edges = [NetDiffEdge('0', '1'), NetDiffEdge('2', '1'), NetDiffEdge('2', '3')]

blue = NLocalLabel('blue')
yellow = NLocalLabel('yellow')
red = NLocalLabel('red')
green = GlobalLabel('green')

nllabels = [blue, yellow, red]
glabels = [green]

nodes[0].setLabels(nllabels)


graph = NetDiffGraph('graph', nodes, edges)
graph.setLabels(glabels)

local_rules = [NetDiffLocalRule(red, [(blue, portion.closed(0.5,1))], 1,
			[(yellow, portion.closed(0,1))], None, Tipping(0.5, portion.closed(0.7, 1)))]

global_rules = [NetDiffGlobalRule(green, blue, [(red, portion.closed(0.5, 1))], Average())]

facts = [NetDiffFact(nodes[1], blue, portion.closed(0.5, 1), 0, tmax), 
		NetDiffFact(nodes[0], yellow, portion.closed(0.5, 1), 0, tmax), 
		NetDiffFact(nodes[2], yellow, portion.closed(0.7, 1), 0, tmax)]



program = NetDiffProgram(graph, tmax, facts, local_rules, global_rules)

interp = program.diffusion()

factoryFact = CFNetDiffFactRedLabels(graph, tmax)

randomFact = factoryFact.getRandomFact()


print(str(interp))
print(randomFact)


