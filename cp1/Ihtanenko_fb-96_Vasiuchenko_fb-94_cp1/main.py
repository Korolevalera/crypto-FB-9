import regex
import collections
import unicodedata
import pandas as pd
import numpy as np
import math

Alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', ' з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
            'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
Alphabet_and_space = [' ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', ' з', 'и', 'й', 'к', 'л', 'м', 'н',
                      'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

book = open(r"D:\Python stuff\Lab1_Crypta\crime_and_punishment.txt", encoding="utf8").read()
book = book.lower().replace("\n", " ")
book = ' '.join(book.split())

text = ''.join(c for c in book if unicodedata.category(c).startswith('L'))

text_with_space = regex.sub(r'[^\w\s]+|[\d]+', r'', book).strip()
print(text_with_space)


words = []
words_and_space = []

for i in range(0, len(text)):
    words.append(text[i])
for i in range(0, len(text_with_space)):
    words_and_space.append(text_with_space[i])

words_count = dict(collections.Counter(words))
words_and_space_count = dict(collections.Counter(words_and_space))

f_words = {k: words_count[k] / len(words) for k in words_count}
f_words_and_space = {k: words_and_space_count[k] / len(words_and_space) for k in words_and_space_count}
print(f_words)

for_index_temp = sorted(f_words, key=lambda x: words_count[x], reverse=1)
for_index_temp2 = sorted(f_words_and_space, key=lambda x: words_and_space_count[x], reverse=1)


tempdict1 = []
tempdict2 = []

for i in range(0, len(for_index_temp)):
    tempdict1.append(f_words[for_index_temp[i]])

for i in range(0, len(for_index_temp2)):
    tempdict2.append(f_words_and_space[for_index_temp2[i]])

dataframe = pd.DataFrame(index=for_index_temp)
dataframe_with_space = pd.DataFrame(index=for_index_temp2)
dataframe['frequency_without_spaces'] = tempdict1
dataframe_with_space['frequency_with_spaces'] = tempdict2
print(dataframe.head(10))
print(dataframe_with_space.head(10))

dataframe.to_excel("freq_with_spaces.xlsx")
dataframe_with_space.to_excel("freq_without_spaces.xlsx")


# Bigram without space
bigram_step_one = []
bigram_step_two = []
for j in range(0, len(text) - 1):
    bigram_step_one.append(text[j] + text[j + 1])

for j in range(0, len(text) - 2, 2):
    bigram_step_two.append(text[j] + text[j + 1])

bigram_step_one_count = dict(collections.Counter(bigram_step_one))
bigram_step_two_count = dict(collections.Counter(bigram_step_two))

f_bigram_step_one_count = {k: bigram_step_one_count[k] / len(bigram_step_one) for k in bigram_step_one_count}
f_bigram_step_two_count = {k: bigram_step_two_count[k] / len(bigram_step_two) for k in bigram_step_two_count}


# Bigram with space
bigram_step_one_with_space = []
bigram_step_two_with_space = []
for j in range(0, len(text_with_space) - 1):
    bigram_step_one_with_space.append(text_with_space[j] + text_with_space[j + 1])

for j in range(0, len(text_with_space) - 2, 2):
    bigram_step_two_with_space.append(text_with_space[j] + text_with_space[j + 1])

bigram_step_one_count_with_space = dict(collections.Counter(bigram_step_one_with_space))
bigram_step_two_count_with_space = dict(collections.Counter(bigram_step_two_with_space))

f_bigram_step_one_count_with_space = {k: bigram_step_one_count_with_space[k] / len(bigram_step_one_with_space) for k in
                                      bigram_step_one_count_with_space}
f_bigram_step_two_count_with_space = {k: bigram_step_two_count_with_space[k] / len(bigram_step_two_with_space) for k in
                                      bigram_step_two_count_with_space}

# H
def H(freq, n):
    temp = []
    for f in freq.values():
        temp.append(f * math.log(f, 2))
    temp = sorted(temp)
    H = -sum(temp) / n
    return H


H2 = H(f_bigram_step_one_count, 2)
H2_step_two = H(f_bigram_step_two_count, 2)
H2_space = H(f_bigram_step_one_count_with_space, 2)
H2_step_two_space = H(f_bigram_step_two_count_with_space, 2)
print(H(f_words, 1))
print(H(f_words_and_space, 1))
print(H2)
print(H2_step_two)
print(H2_space)
print(H2_step_two_space)


def matrix_(Alphabet, freq):
    matrix = pd.DataFrame(index=Alphabet, columns=Alphabet)
    maska_ = []

    for i in Alphabet:
        for j in Alphabet:
            maska_.append(i + j)
    n = 0

    for i in range(0, len(Alphabet)):
        matrix[Alphabet[i]] = maska_[n:len(Alphabet) + n]
        n = len(Alphabet) + n
    matrix = matrix.T

    for key in list(freq.keys()):
        a, c = np.where(matrix == key)
        matrix.iloc[a, c] = freq[key]

    for m in maska_:
        a, c = np.where(matrix == m)
        matrix.iloc[a, c] = 0
    return matrix

matrix_bigram_step_one = matrix_(Alphabet, f_bigram_step_one_count)
matrix_bigram_step_two = matrix_(Alphabet, f_bigram_step_two_count)
matrix_bigram_step_one_with_space = matrix_(Alphabet_and_space, f_bigram_step_one_count_with_space)
matrix_bigram_step_two_with_space = matrix_(Alphabet_and_space, f_bigram_step_two_count_with_space)

matrix_bigram_step_one.to_excel("matrix_bigram_step_one.xlsx")
matrix_bigram_step_two.to_excel("matrix_bigram_step_two.xlsx")
matrix_bigram_step_one_with_space.to_excel("matrix_bigram_step_one_with_space.xlsx")
matrix_bigram_step_two_with_space.to_excel("matrix_bigram_step_two_with_space.xlsx")


def R(value):
    R_ = 1 - value / math.log(33, 2)
    print(R_)
    return (R_)

R(2.468021)
R(3.055857)
R(2.933340)
R(3.403532)
R(1.535043)
R(2.131663)