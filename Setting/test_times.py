import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from datetime import datetime
import mysql.connector
import random
import string
from Ontological.NetDERKB import NetDERKB
from Ontological.NetDERChase import NetDERChase
from Ontological.NetDERQuery import NetDERQuery
from Ontological.Atom import Atom
from Ontological.Variable import Variable
from Ontological.Constant import Constant

mydb = mysql.connector.connect(
  host="localhost",
  database="test"
)

def insert_rows_DB(mydb, values):
	mycursor = mydb.cursor()
	sql = "INSERT INTO p (X, Y) VALUES (%s, %s)"

	mycursor.executemany(sql, values)

	mydb.commit()

	print(mycursor.rowcount, "was inserted.")

def get_rand_word(max_size):
	result = ''
	size = random.randint(0,max_size)
	for index in range(size):
		lower_upper_alphabet = string.ascii_letters
		random_letter = random.choice(lower_upper_alphabet)
		result += random_letter
	return result

def get_rand_words(cant, max_size):
	result = []
	for index in range(cant):
		w = get_rand_word(max_size)
		while w in result:
			w = get_rand_word(max_size)
		result.append(w)
	return result

inicio1 = datetime.now()
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM p")

myresult = mycursor.fetchall()

answers1 = []
for (x,y) in myresult:
	answers1.append({'X':x, 'Y':y})
fin1 = datetime.now()

atoms = []
for (x,y) in myresult:
	atoms.append(Atom('p', [Constant(x), Constant(y)]))


query1 = NetDERQuery(ont_cond = [Atom('p', [Variable('X'), Variable('Y')])])
kb = NetDERKB(ont_data = atoms)
chase = NetDERChase(kb)

inicio2 = datetime.now()
answers2 = chase.answer_query(query1, 1)
fin2 = datetime.now()

print('len(answers1)', len(answers1))
print('len(answers2)', len(answers2))
print('query con traduccion SQL', fin1 - inicio1)
print('query con homomorfismos', fin2 - inicio2)

'''
val = []

words = get_rand_words(32000, 10)

for index in range(int(len(words)/2)):
	val.append((words[2*index], words[2*index + 1]))


insert_rows_DB(mydb, val)'''
