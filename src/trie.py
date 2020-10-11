class Trie(object):
	class TrieNode(object):
		def __init__(self, char=''):
			self._char = char
			self._children = {}
			self._positions = []
			self._count_number = 0

		def get_char(self):
			return self._char

		def get_childrens(self):
			return self._children

		def get_count_number(self):
			return self._count_number

		def add_child(self, child):
			self._children[child.get_char()] = child

		def increment_counter(self):
			self._count_number += 1

		def add_position(self, position):
			self._positions.append(position)

		def get_positions(self):
			return self._positions

		def __eq__(self, other):
			if not isinstance(other, Trie.TrieNode):
				raise TypeError("cvor trie-a mora biti TrieNode objekat")
			return self._char == other._char

		def __str__(self):
			print("(Char:{0} Count:{1})".format(self.get_char(),  self.get_count_number()))

	# -----------------main methods-----------------------------------------
	def __init__(self, words):
		self._root = self.TrieNode()
		self._words = words
		self._fill_trie_with_words()

	def _fill_trie_with_words(self):
		for position in range(len(self._words)):
			self._insert(self._words[position].lower(), position)

	def _insert(self, word, position):
		chars = list(word)
		current_node = self._root
		for index, char in enumerate(chars):
			if char in current_node.get_childrens():
				node = current_node.get_childrens()[char]
				if index == (len(chars) - 1):
					node.increment_counter()
					node.add_position(position)
				current_node = node
			else:
				new_node = self.TrieNode(char)
				if index == (len(chars) - 1):
					new_node.increment_counter()
					new_node.add_position(position)
				current_node.add_child(new_node)
				current_node = new_node

	def _get_last_node_of_word(self, word):
		chars = list(word)
		current_node = self._root
		for index, char in enumerate(chars):
			if char in current_node.get_childrens():
				node = current_node.get_childrens()[char]
				if index == (len(chars) - 1):
					return node
				current_node = node
			else:
				return None

	def get_counter_for_word(self, word):
		if len(word.split()) > 1:
			positions, counter = self.__counter_and_positions_for_phrase(word)
			return counter
		node = self._get_last_node_of_word(word)
		if node is None:
			return 0
		return node.get_count_number()

	def get_positions_for_word(self, word):
		if len(word.split()) > 1:
			positions, counter = self.__counter_and_positions_for_phrase(word)
			return positions
		node = self._get_last_node_of_word(word)
		if node is None:
			return []
		return node.get_positions()

	def __counter_and_positions_for_phrase(self, phrase):
		ret_val_positions = []
		ret_val_counter = 0

		words = phrase.split()
		words = list(map(lambda token: token.strip().lower(), words))
		first_word_indexes = self.get_positions_for_word(words[0])
		for i in first_word_indexes:
			found = True
			for j in range(1, len(words)):
				if i + j < len(self._words):
					if words[j] != self._words[i + j].lower():
						found = False
						break
			if found:
				list_to_extend = [i]
				for k in range(1, len(words)):
					list_to_extend.append(k + i)
				ret_val_positions.extend(list_to_extend)
				ret_val_positions = list(set(ret_val_positions))
				ret_val_counter += 1

		return ret_val_positions, ret_val_counter

	def get_words_for_autocomplete(self, word):
		retList = []
		current_node = self._get_last_node_of_word(word)
		if current_node is None:
			return retList

		counter = 0

		def fill_autocomplete_list(node, base_word):
			nonlocal counter
			for child in node.get_childrens().values():
				if counter > 10:
					return retList
				base_word += child.get_char()
				if child.get_count_number() > 0:
					retList.append(base_word)
					counter += 1
				fill_autocomplete_list(child, base_word)
				base_word = base_word[:-1]

		fill_autocomplete_list(current_node, word)

		return list(set(retList))
