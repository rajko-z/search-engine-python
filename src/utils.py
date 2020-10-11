import pickle
import parser_html
from glob import iglob
import make_graph
import os

def make_allwords_file():

	parser = parser_html.Parser()

	file_list = [f for f in iglob('python-3.8.3-docs-html/**/*', recursive=True) if os.path.isfile(f)]
	allwords = open("allwords.txt", "w+", encoding='utf-8')

	huge_list = []
	for file in file_list:
		if file.endswith(".html") or file.endswith(".htm"):
			links, words = parser.parse(file)
			huge_list.extend(words)

	huge_list = list(set(huge_list))
	brrr = 0
	for item in huge_list:
		if brrr == 30:
			brrr = 0
			allwords.write(item.lower() + '\n')
		else:
			brrr += 1
			allwords.write(item.lower() + ' ')

	allwords.close()


def make_graph_serialization_bin():
	make_graph.load_graph()
	binary_file = open('graph_serialization.bin', 'wb')
	serialized_graph = pickle.dump(make_graph.graph, binary_file)
	binary_file.close()


"""

make_graph_serialization_bin()

By running this function from this module, you are making graph_serialization.bin
which you can letter use when running the program.
You don't have to load all files and make graph again, you just use serialization to speed up
the proces
	
"""
