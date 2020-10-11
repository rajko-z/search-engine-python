import make_graph
from colors import Colors
import shlex
import os
os.system("")
ODUSTANAK = "x"


def cant_find_suggestion():
	print(Colors.YELLOW + Colors.BOLD + "Hmm... it seems like there is no suggestions for this input. Check your input and try again." + Colors.RESET)


def autocomplete_is_enabled(text):
	text = text.strip()
	return text[len(text)-1] == '*'


def _invalid_autocomplete_format(text):
	text = text.replace(" ", "")
	text = text[::-1]
	for index in range(len(text)-1):
		if text[index] == '*':
			if text[index + 1] == "'" or text[index + 1] == '"':
				return True
			if text[index + 1] != '*':
				return False


def _get_autocompleted_text(text):

	def _get_word_for_autocomplete(text):
		words = shlex.split(text)
		last_word = words[len(words) - 1]
		if last_word.endswith("*") and last_word != "*":
			return last_word[:-1].strip().lower()
		return words[len(words) - 2].strip().lower()

	def _get_ending_words(word):
		ret_list = []
		for page in make_graph.graph.pages():
			if len(ret_list) > 10:
				break
			ret_list.extend(page.get_words_for_autocomplete(word))
			ret_list = list(set(ret_list))
		return list(set(ret_list[:10]))

	def _get_prefix(text):

		def _calculate_prefix(words):
			ret_val = ""
			for word in words:
				if len(word.split()) > 1:
					ret_val += "'" + word + "' "
				else:
					ret_val += word + " "
			return ret_val[:-1]

		words = shlex.split(text)
		if words[len(words) - 1].endswith("*") and words[len(words) - 1] != "*":
			return _calculate_prefix(words[:-1])
		return _calculate_prefix(words[:-2])

	def _get_final_recomendations(prefix, ending_words):
		ret_list = []
		for word in ending_words:
			ret_list.append(prefix + " " + word)
		return ret_list

	word = _get_word_for_autocomplete(text)
	ending_words = _get_ending_words(word)
	prefix = _get_prefix(text)
	return _get_final_recomendations(prefix, ending_words)


def _print_recomendations(listt):
	for index, item in enumerate(listt):
		print(Colors.BOLD + Colors.BLUE + str(index + 1) + ". " + item + Colors.RESET)


def _calculate_indexes(listt):
	indexes = [i for i in range(1, len(listt) + 1)]
	return list(map(lambda item: str(item), indexes))


def get_auto_completed_text(text):
	if _invalid_autocomplete_format(text):
		return False, " "

	recomendations = _get_autocompleted_text(text)

	if len(recomendations) == 0:
		return False, " "

	indexes = _calculate_indexes(recomendations)
	_print_recomendations(recomendations)

	while True:
		inn = input("Enter the number of the desired text (or x to exit) >> ")
		inn = inn.strip().lower()
		if inn in indexes:
			return True, recomendations[int(inn) - 1]
		if inn == 'x':
			return False, ODUSTANAK
