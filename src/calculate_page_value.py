import make_graph

class PageValue(object):

	def __init__(self, page, value=0, indexes=None):
		if indexes is None:
			indexes = []
		self._page = page
		self._value = value
		self._indexes = indexes

	def value(self):
		return self._value

	def set_value(self, value):
		self._value = value

	def add_index(self, index):
		self._indexes.extend(index)

	def indexes(self):
		return self._indexes

	def page(self):
		return self._page


class WordFinder(object):

	__slots__ = '_word', '_must', '_never', '_no_preference'

	def __init__(self, word,  must=False, never=False, no_preference=True):
		self._word = word
		self._must = must
		self._never = never
		self._no_preference = no_preference

	def must(self):
		return self._must

	def never(self):
		return self._never

	def no_preference(self):
		return self._no_preference

	def word(self):
		return self._word


def _add_value_from_links(page, word):
	ret_val = 0
	for link_page in make_graph.graph.get_inout_pages(page, False):
		ret_val += link_page.get_counter_for_word(word)
	return ret_val


def _get_word_rank(page, word):
	word_counter = page.get_counter_for_word(word)
	if word_counter > 0:
		word_rank = word_counter * 5
		word_rank += _add_value_from_links(page, word)
		return word_rank
	return 0


def _page_contains_NOT_word(page, wordfinderr):
	if wordfinderr.never() and page.get_counter_for_word(wordfinderr.word()) > 0:
		return True
	return False


def _page_doesnt_contain_AND_word(page, wordfinderr):
	if wordfinderr.must() and page.get_counter_for_word(wordfinderr.word()) == 0:
		return True
	return False


def _evaluate_page(page, wordfinder_objs):
	all_rank = 0
	all_positions = []

	for wordfinder in wordfinder_objs:
		if _page_contains_NOT_word(page, wordfinder) or _page_doesnt_contain_AND_word(page, wordfinder):
			return None

	for wordfinder in wordfinder_objs:
		if not wordfinder.never():
			all_rank += _get_word_rank(page, wordfinder.word())
			all_positions.extend(page.get_positions_for_word(wordfinder.word()))

	if all_rank == 0:
		return None
	page_value_obj = PageValue(page, all_rank, all_positions)
	return page_value_obj


def _get_prepared_words_for_search(words):

	def check_and_add_to_dict(word):
		if word not in seen:
			seen[word] = WordFinder(word)

	def check_and_add_element_for_AND_operator(indexx):
		if words[indexx] in seen:
			if not seen[words[indexx]].never():
				seen[words[indexx]] = WordFinder(words[indexx], True)
		else:
			seen[words[indexx]] = WordFinder(words[indexx], True)

	def check_and_add_element_for_OR_operator(indexx):
		if words[indexx] not in seen:
			seen[words[indexx]] = WordFinder(words[indexx])

	seen = {}
	index = 0
	while index < len(words):
		if words[index] != 'and' and words[index] != 'not' and words[index] != 'or':
			check_and_add_to_dict(words[index])
			index += 1
		elif words[index] == 'and':
			if index == 0 or index == len(words) - 1:
				check_and_add_to_dict('and')
				index += 1
			else:
				check_and_add_element_for_AND_operator(index - 1)
				check_and_add_element_for_AND_operator(index + 1)
				index += 2
		elif words[index] == 'or':
			if index == 0 or index == len(words) - 1:
				check_and_add_to_dict('or')
				index += 1
			else:
				check_and_add_element_for_OR_operator(index + 1)
				index += 2
		elif words[index] == 'not':
			if index == len(words) - 1:
				check_and_add_to_dict('not')
				index += 1
			else:
				seen[words[index + 1]] = WordFinder(words[index + 1], False, True, True)
				index += 2
	return seen.values()


def get_pages(text):
	import shlex
	words = shlex.split(text)
	words = list(map(lambda token: token.strip().lower(), words))
	wordfinder_objs = _get_prepared_words_for_search(words)

	pages_values = []

	for page in make_graph.graph.pages():
		page_value_obj = _evaluate_page(page, wordfinder_objs)
		if page_value_obj is not None:
			pages_values.append(page_value_obj)

	pages_values = sorted(pages_values, key=lambda obj: (obj.value(), make_graph.graph.get_num_of_inout_pages(obj.page(), False)), reverse=True)
	return pages_values
