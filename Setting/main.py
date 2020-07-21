import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import subprocess
import random
import csv
from tempfile import NamedTemporaryFile
import shutil
from BadBot import BadBot
from AFPublication import AFPublication
from CFPublicationNBM import CFPublicationNBM

def update_categories():
	filename = "Datasets/Fake_news/fake-news-detection/data.csv"
	tempfile = NamedTemporaryFile(mode='a', delete=False, newline='', encoding='utf-8')

	fieldnames = ['ID', 'URLs', 'Headline', 'Body', 'Label', 'Category']
	total_categories = ["A", "B", "C", "D", "E"]


	with open(filename, 'r', newline='', encoding='utf-8') as csvfile, tempfile:
	    reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter = ",")
	    next(reader, None)  # skip the headers
	    writer = csv.DictWriter(tempfile, fieldnames=fieldnames, delimiter = ",")
	    writer.writeheader()
	    contador = 0
	    for row in reader:
	    	index = random.randint(0, len(total_categories) - 1)
	    	writer.writerow({'ID': contador, 'URLs': row['URLs'], 'Headline': row['Headline'], 'Body': row['Body'], 'Label': row['Label'], 'Category': total_categories[index]})
	    	contador += 1

	shutil.move(tempfile.name, filename)

#update_categories()


badBot = BadBot()

trace = badBot.get_trace()
print("------------------Traza 1-----------------")
print(trace)
print("AFPublication.num_new_posts", AFPublication.num_new_posts)
print("AFPublication.num_share_posts", AFPublication.num_share_posts)
print("AFPublication.num_share_posts2", AFPublication.num_share_posts2)
print("AFPublication.num_mal_posts", CFPublicationNBM.num_mal_posts)
trace = badBot.get_trace()
print("------------------Traza 2-----------------")
print(trace)

print("AFPublication.num_new_posts", AFPublication.num_new_posts)
print("AFPublication.num_share_posts", AFPublication.num_share_posts)
print("AFPublication.num_share_posts2", AFPublication.num_share_posts2)
print("AFPublication.num_mal_posts", CFPublicationNBM.num_mal_posts)

#subprocess.call(["executable/PaRMAT.exe", "-nEdges", "15", "-nVertices", "15", "-noEdgeToSelf", "-noDuplicateEdges", "-output", "graph_structure/graph(n=15, e=15).csv"])
