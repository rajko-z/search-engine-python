import autocomplete
import calculate_page_value
import did_you_mean
import make_graph
import pages_view
import validator


def cant_find_page():
	print("Can't find pages :(  Check your input, or try with more general words")


def try_to_find_pages(text):
	pages = calculate_page_value.get_pages(text.strip())
	if len(pages) == 0:
		cant_find_page()
	else:
		pages_view.show_pages(pages, 0, 1, 1)


def search():
	while True:
		print()
		print("_" * 50)
		text = input("Input text (x to close) ->> ")
		if text == "x":
			return
		if validator.validate_input(text):

			if autocomplete.autocomplete_is_enabled(text):
				possible, text = autocomplete.get_auto_completed_text(text.strip())
				if text == autocomplete.ODUSTANAK:
					continue
				if not possible:
					autocomplete.cant_find_suggestion()
					continue
			else:
				text = did_you_mean.ask_and_get_did_you_mean_text(text.strip())

			try_to_find_pages(text.strip())


def setup():
	print("Loading...")


def info():
	print('+==================================================================================================+\n'
	      '|                                        SEARCH ENGINE                                             |\n'     
	      '+==================================================================================================+\n'
	      '| This is the search engine based on python-3.8.3-docs html files                                  |\n'
	      '|                                                                                                  |\n'
	      '| What\'s available:                                                                                |\n'
	      '| - it\'s case insensitive                                                                          |\n'
	      '|                                                                                                  |\n'
	      '| - You can input one or more words for standard searching and you will get number of results      |\n'
	      '|   and ranked pages which you can scroll down                                                     |\n'
	      '|                                                                                                  |\n'
	      '| - You can type phrases like \'python is great\' with single or double quotes. You will only get    |\n'
	      '|   pages that contain phrase in the exact order of words                                          |\n'
	      '|                                                                                                  |\n'
	      '| - Operators OR AND NOT are allowed with order of importance NOT > AND > OR                       |\n'
	      '|   For example if you type >> tuple and dictionary not list  >> you will get pages that contains  |\n'
	      '|   tuple and dictionary but doesn\'t contain list as a word                                        |\n'
	      '|   Or if you type >> zip or tar >> you will get pages that contains either zip or tar word or both|\n'
	      '|   You can combine operators with respect of their importance                                     |\n'
	      '|                                                                                                  |\n'
	      '| - Did you mean feature. If you misspelled the word, you will get correction.                     |\n'
	      '|   For example, if you type pytin, question will be >> Did you mean: python (yes/no)?             |\n'
	      '|                                                                                                  |\n'
	      '| - Autocomplete feature: start to type somethin and input * at the and of text, you will get      |\n'
	      '|   recommendations.                                                                               |\n'
	      '|   For example:  >> download or pyth* , and one of possibilities will be download or python       |\n'
	      '+--------------------------------------------------------------------------------------------------+\n')


def main():
	# if you want to run graph for the first time, or you have made
	# some changes, then run make graph like this
	# make_graph.load_graph()

	# if you want to use graph serialization then use it like this
	make_graph.load_graph_from_bin()
	info()
	search()


if __name__ == '__main__':
	main()
