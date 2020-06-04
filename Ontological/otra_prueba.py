from NetDERQuery import NetDERQuery
from Variable import Variable
from Atom import Atom

atoms = [Atom('a', [Variable('X'), Variable('Y')]), Atom('b', [Variable('B'), Variable('B')]), Atom('c', [Variable('X'), Variable('B')]) ]
q1 = NetDERQuery(exist_var = [Variable('X'), Variable('Y'), Variable('Z')], ont_cond = atoms)

queries = q1.get_disjoint_queries()

index = 0
for q in queries:
	print('query:', index)
	print('len(q.get_ont_body():', len(q.get_ont_body()))
	for atom in q.get_ont_body():
		print(str(atom))

	for var in q.get_exist_var():
		print('existential variables')
		print(str(var))

	index += 1
