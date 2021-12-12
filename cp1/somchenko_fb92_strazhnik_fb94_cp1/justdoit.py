import re
from collections import Counter
from math import log2

file = open('source.txt', encoding='cp1251')
report = open('report.txt', 'w')
text = file.read()
text_with_spaces = re.sub(r'[^а-яА-Я ]', '', text).lower()
text_without_spaces = re.sub(r'[^а-яА-Я]', '', text).lower()


def letters_frequency(_text):
    frequency = Counter(_text)
    for key in frequency.keys():
        frequency[key] /= len(_text)
    frequency = dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))
    return frequency


def bigrams_frequency(_text):
    frequency = Counter(_text[bi: bi + 2] for bi in range(len(_text) - 1))
    for key in frequency.keys():
        frequency[key] /= len(_text)
    frequency = dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))
    return frequency


def bigrams_wo_intersection_frequency(_text):
    frequency = Counter(_text[bi: bi + 2] for bi in range(0, len(_text) - 1, 2))
    for key in frequency.keys():
        frequency[key] /= len(_text)
    frequency = dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))
    return frequency


def entropy(frequency):
    _entropy = 0
    for value in frequency.values():
        _entropy += -value * log2(value)
    return _entropy


def redundancy(_entropy, quantity):
    return 1 - _entropy / log2(quantity)


def output(var):
    for letter in var:
        report.write(f'{letter} -- {str(var[letter])}\n')
    report.write(f'\n\n')


letters_w_spaces_frequency = letters_frequency(text_with_spaces)
letters_wo_spaces_frequency = letters_frequency(text_without_spaces)
bigrams_w_spaces_frequency = bigrams_frequency(text_with_spaces)
bigrams_wo_spaces_frequency = bigrams_frequency(text_without_spaces)
bigrams_w_spaces_wo_intersections_frequency = bigrams_wo_intersection_frequency(text_with_spaces)
bigrams_wo_spaces_wo_intersections_frequency = bigrams_wo_intersection_frequency(text_without_spaces)

letters_w_spaces_entropy = entropy(letters_w_spaces_frequency)
letters_wo_spaces_entropy = entropy(letters_wo_spaces_frequency)
bigrams_w_spaces_entropy = entropy(bigrams_w_spaces_frequency) / 2
bigrams_wo_spaces_entropy = entropy(bigrams_wo_spaces_frequency) / 2
bigrams_w_spaces_wo_intersections_entropy = entropy(bigrams_w_spaces_wo_intersections_frequency) / 2
bigrams_wo_spaces_wo_intersections_entropy = entropy(bigrams_wo_spaces_wo_intersections_frequency) / 2

letters_w_spaces_redundancy = redundancy(letters_w_spaces_entropy, 33)
letters_wo_spaces_redundancy = redundancy(letters_wo_spaces_entropy, 32)
bigrams_w_spaces_redundancy = redundancy(bigrams_w_spaces_entropy, 33)
bigrams_wo_spaces_redundancy = redundancy(bigrams_wo_spaces_entropy, 32)
bigrams_w_spaces_wo_intersections_redundancy = redundancy(bigrams_w_spaces_wo_intersections_entropy, 33)
bigrams_wo_spaces_wo_intersections_redundancy = redundancy(bigrams_wo_spaces_wo_intersections_entropy, 32)

report.write(f'Entropy:\n'
             f'Letters with spaces:\n{letters_w_spaces_entropy}\n'
             f'Letters without spaces:\n{letters_wo_spaces_entropy}\n'
             f'Bigrams with spaces:\n{bigrams_w_spaces_entropy}\n'
             f'Bigrams without spaces:\n{bigrams_wo_spaces_entropy}\n'
             f'Bigrams with spaces, without intersections:\n{bigrams_w_spaces_wo_intersections_entropy}\n'
             f'Bigrams without spaces, without intersections:\n{bigrams_wo_spaces_wo_intersections_entropy}\n\n')

report.write(f'Redundancy:\n'
             f'Letters with spaces:\n{letters_w_spaces_redundancy}\n'
             f'Letters without spaces:\n{letters_wo_spaces_redundancy}\n'
             f'Bigrams with spaces:\n{bigrams_w_spaces_redundancy}\n'
             f'Bigrams without spaces:\n{bigrams_wo_spaces_redundancy}\n'
             f'Bigrams with spaces, without intersections:\n{bigrams_w_spaces_wo_intersections_redundancy}\n'
             f'Bigrams without spaces, without intersections:\n{bigrams_wo_spaces_wo_intersections_redundancy}\n\n')

report.write(f'Letters with spaces frequency:\n')
output(letters_w_spaces_frequency)
report.write(f'Letters without spaces frequency:\n')
output(letters_wo_spaces_frequency)
report.write(f'Bigrams with spaces frequency:\n')
output(bigrams_w_spaces_frequency)
report.write(f'Bigrams without spaces frequency:\n')
output(bigrams_wo_spaces_frequency)
report.write(f'Bigrams with spaces, without intersections frequency:\n')
output(bigrams_w_spaces_wo_intersections_frequency)
report.write(f'Bigrams without spaces, without intersections frequency:\n')
output(bigrams_wo_spaces_wo_intersections_frequency)
