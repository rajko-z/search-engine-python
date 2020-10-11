from colors import Colors
import os
os.system("")

MAX_LEN_OF_WORD = 45


def _word_is_empty(word):
	if word is None or word == "":
		print(Colors.RED + "Error. Phrase between quotes is empty." + Colors.RESET)
		return True
	return False


def _word_is_to_long(word):
	sub_words = word.split()
	for sub_word in sub_words:
		if len(sub_word) > MAX_LEN_OF_WORD:
			print(Colors.RED + "Error. It seems like there is a word which is to long , try something else." + Colors.RESET)
			return False


def validate_input(text):
	if text == "":
		print(Colors.RED + "Error. Please input text for search." + Colors.RESET)
		return False
	try:
		import shlex
		words = shlex.split(text)
		words = list(map(lambda item: item.strip(), words))
		for word in words:
			if _word_is_empty(word):
				return False
			if _word_is_to_long(word):
				return False
	except ValueError:
		print(Colors.RED + "Error. Invalid use of phrases. Use format as \"text phrase\" or 'text phrase'" + Colors.RESET)
		return False

	return True
