from colors import Colors
import os
os.system("")

MAX_COLORED_WORDS = 5
NUMBER_PER_PAGE = 5


def _print_page_header(page, file_counter):
	print()
	print(Colors.UNDERLINE + Colors.BOLD + Colors.BLUE + str(file_counter) + ". " + page.get_filePath() + Colors.RESET)


def _print_page(page_value, file_counter):
	_print_page_header(page_value.page(), file_counter)

	indexes = page_value.indexes()
	words = page_value.page().get_words()

	printed_indexes = {}

	br = 0
	words_in_line = 0
	for index in indexes:
		br += 1
		if br == MAX_COLORED_WORDS:
			break
		for i in range(index-10, index+10):
			if 0 <= i <= (len(words) - 1) and i not in printed_indexes:
				if words_in_line <= 17:
					if i in indexes:
						print(Colors.GREEN + Colors.BOLD + words[i] + Colors.RESET, end=' ')
					else:
						print(words[i], end=' ')
					words_in_line += 1
				else:
					if i in indexes:
						print(Colors.GREEN + Colors.BOLD + words[i] + Colors.RESET)
					else:
						print(words[i])
					words_in_line = 0
				printed_indexes[i] = i
	print()


def _want_another_view_page():
	print()
	while True:
		choice = input(Colors.BLINK + Colors.YELLOW + "Press ENTER to go to next page or x to stop searching... " + Colors.RESET)
		if choice == "":
			return True
		elif choice == "x":
			return False


def _calculate_num_of_pages(size):
	if size % NUMBER_PER_PAGE == 0:
		ret_val = size // NUMBER_PER_PAGE
	elif size < NUMBER_PER_PAGE:
		ret_val = 1
	else:
		ret_val = (size // NUMBER_PER_PAGE) + 1
	return ret_val


def _print_page_number(pages, page_number):
	num_of_pages = _calculate_num_of_pages(len(pages))
	print()
	print(Colors.OKBLUE + 'Results:{0} Page({1}/{2}):'.format(len(pages), page_number, num_of_pages) + Colors.RESET)


def show_pages(pages, starting_index, page_number, file_counter):
	_print_page_number(pages, page_number)
	counter = 0
	end_index = starting_index
	for index in range(starting_index, len(pages)):
		_print_page(pages[index], file_counter)
		file_counter += 1
		counter += 1

		if counter == NUMBER_PER_PAGE or index == (len(pages) - 1):
			end_index = index + 1
			break

	if counter < NUMBER_PER_PAGE or end_index == len(pages):
		return

	if _want_another_view_page():
		page_number += 1
		show_pages(pages, end_index, page_number, file_counter)
	else:
		return
