"""
 Implementation of did you mean feature based on probability
 Source code from : http://www.norvig.com/spell-correct.html
 It uses 'allwords.txt' to calculate possible corrections for word
"""

import re
from collections import Counter


def words(text): return re.findall(r'\w+', text.lower())


WORDS = Counter(words(open('../allwords.txt', encoding='utf-8').read()))


def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N


def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)


def candidates(word):
    "Generate possible spelling corrections for word."
    return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]


def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


"""-----------------------------------------------------------------------------------"""


def _check_phrase_did_you_mean(sub_words_in_phrase):
    ret_text = "'"
    for index in range(len(sub_words_in_phrase)):
        sub_word = sub_words_in_phrase[index].lower()
        correct = correction(sub_word)
        if correct != sub_word:
            ret_text += correct
        else:
            ret_text += sub_word
        if index == (len(sub_words_in_phrase) - 1):
            ret_text += "' "
        else:
            ret_text += " "
    return ret_text


def _check_word_did_you_mean(word):
    correct = correction(word)
    if correct != word:
        return correct + " "
    return word + " "


def _get_new_did_you_mean_text_if_possible(text):
    import shlex
    words = shlex.split(text.strip())
    words = list(map(lambda item: item.strip().lower(), words))
    ret_text = ""
    for word in words:
        sub_words_in_phrase = word.split()
        if len(sub_words_in_phrase) > 1:
            ret_text += _check_phrase_did_you_mean(sub_words_in_phrase)
        else:
            ret_text += _check_word_did_you_mean(word)
    return ret_text.strip()


def ask_and_get_did_you_mean_text(text):
    from colors import Colors
    new_text = _get_new_did_you_mean_text_if_possible(text)
    if new_text == text.lower():
        return text
    color_setup = Colors.ITALIC + Colors.UNDERLINE + Colors.BOLD + Colors.BLUE
    question = color_setup + "Did you mean: {}".format(new_text) + Colors.RESET + "(yes/no)? "
    while True:
        inn = input(question)
        inn = inn.lower()
        if inn == 'yes' or inn == 'y':
            return new_text
        if inn == 'no' or inn == 'n':
            return text
