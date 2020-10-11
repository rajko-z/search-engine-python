from trie import Trie


class Graph(object):
	class Page(object):
		def __init__(self, filePath, words=None):
			if words is None:
				words = []
			self._filePath = filePath
			self._words = words
			self._trie = Trie(words)

		def get_filePath(self):
			return self._filePath

		def get_words(self):
			return self._words

		def get_counter_for_word(self, word):
			return self._trie.get_counter_for_word(word)

		def get_positions_for_word(self, word):
			return self._trie.get_positions_for_word(word)

		def get_words_for_autocomplete(self, word):
			return self._trie.get_words_for_autocomplete(word)

		def __hash__(self):
			return hash(id(self))

		def __str__(self):
			return self._filePath

	class Edge(object):

		__slots__ = '_origin', '_destination', '_element'

		def __init__(self, origin, destination, element=None):
			self._origin = origin
			self._destination = destination
			self._element = element

		def opposite(self, page):
			if not isinstance(page, Graph.Page):
				raise TypeError('page must be instance of Graph')
			if self._destination == page:
				return self._origin
			elif self._origin == page:
				return self._destination
			raise ValueError('page not belongs to Graph')

		def element(self):
			return self._element

		def __hash__(self):
			return hash((self._origin, self._destination))

	"""-------------------------Main methods-----------------------------"""

	def __init__(self, directed=False):
		self._outgoing = {}
		self._incoming = {} if directed else self._outgoing
		# cuvam pages po linkovima
		self._links = {}

	def is_directed(self):
		return self._incoming is not self._outgoing

	def _validate_page(self, page):
		if not isinstance(page, self.Page):
			raise TypeError('page is not instance of Graph.Page')
		if page not in self._outgoing:
			raise ValueError('page not belongs to graph')

	def pages(self):
		return self._outgoing.keys()

	def links_dict(self):
		return self._links

	def get_page_by_link(self, link):
		if link not in self._links:
			return None
		return self._links[link]

	def get_num_of_pages(self):
		return len(self._outgoing)

	def get_num_of_edges(self):
		total = sum(len(self._outgoing[page]) for page in self._outgoing)
		return total if self.is_directed() else total // 2

	def edges(self):
		result = set()
		for secondary_map in self._outgoing.values():
			result.update(secondary_map.values())
		return result

	def get_edge(self, p, k):
		self._validate_page(p)
		self._validate_page(k)
		return self._outgoing[p].get(k)

	def get_num_of_inout_pages(self, page, outgoing=True):
		self._validate_page(page)
		adj = self._outgoing if outgoing else self._incoming
		return len(adj[page])

	def get_inout_pages(self, page, outgoing=True):
		self._validate_page(page)
		adj = self._outgoing if outgoing else self._incoming
		for edge in adj[page].values():
			yield edge.opposite(page)

	def insert_page(self, filePath, words):
		page = self.Page(filePath, words)
		self._outgoing[page] = {}
		if self.is_directed():
			self._incoming[page] = {}
		self._links[filePath] = page
		return page

	def insert_edge(self, p, k, element=None):
		if self.get_edge(p, k) is not None:
			raise ValueError('p and k are already adjacent')
		new_edge = self.Edge(p, k, element)
		self._outgoing[p][k] = new_edge
		self._incoming[k][p] = new_edge
