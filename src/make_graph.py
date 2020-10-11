from graph import Graph
import os
import pickle
from glob import iglob
from parser_html import Parser

graph = Graph(True)

def load_graph_from_bin():
	global graph
	graph = pickle.load(open("../graph_serialization.bin", "rb"))


def load_graph():
	global graph
	file_list = [f for f in iglob('../python-3.8.3-docs-html/**/*', recursive=True) if os.path.isfile(f)]

	parser = Parser()

	temp_dict = {}
	for file in file_list:
		if file.endswith(".html") or file.endswith(".htm"):
			links, words = parser.parse(file)
			file = os.path.abspath(file)
			inserted_page = graph.insert_page(file, words)
			temp_dict[inserted_page] = links

	for page, linkovi in temp_dict.items():
		for link in linkovi:
			graph.insert_edge(page, graph.get_page_by_link(link))

