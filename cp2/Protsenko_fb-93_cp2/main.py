import re
from collections import defaultdict

Token = {
    'key2': 'ох', 'key3': 'аут', 'key4': 'ажур', 'key5': 'банка', 'key10': 'самозапись', 'key11': 'фантастично',
    'key12': 'обдурачивать', 'key13': 'легкодумность', 'key14': 'цельнозерновой',
    'key15': 'импровизировать', 'key16': 'металлопрокатный',
    'key17': 'транспортабельный', 'key18': 'внешнеполитический', 'key19': 'алгоритмизированный',
    'key20': 'воздухонепроницаемый'}

with open('version8.txt', 'r', encoding='utf-8') as txt1:
    version8 = re.sub('[^а-я]+', '', txt1.read().lower().replace("ё", "е"))
with open('my_file.txt', 'r', encoding='utf-8') as txt2:
    my_file = re.sub('[^а-я]+', '', txt2.read().lower().replace("ё", "е"))

grammar = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

LetterToIndex = dict(zip(grammar, range(len(grammar))))
IndexToLetter = dict(zip(range(len(grammar)), grammar))


def CipherText(plaintext: str, key: str) -> str:
    encrypted = ''
    split_plaintext = [plaintext[i:i + len(key)] for i in range(0, len(plaintext), len(key))]
    for e_split in split_plaintext:
        i = 0
        for letter in e_split:
            number = (LetterToIndex[letter] + LetterToIndex[key[i]]) % len(grammar)
            encrypted += IndexToLetter[number]
            i += 1
    return encrypted


def OriginalText(dectext: str, key: str) -> str:
    decrypted = ''
    split_dectext = [dectext[i:i + len(key)] for i in range(0, len(dectext), len(key))]
    for e_split in split_dectext:
        i = 0
        for letter in e_split:
            number = (LetterToIndex[letter] - LetterToIndex[key[i]]) % len(grammar)
            decrypted += IndexToLetter[number]
            i += 1
    return decrypted


def amount(content: str) -> dict:
    result = defaultdict(int)
    for char in list(content):
        result[char] += 1
    return dict(result)


def СomplIndex(content: str) -> float:
    score = 0
    for i in amount(content).values():
        score += i * (i - 1)
    return score / (len(content) * (len(content) - 1))


def BuildChunk(content: str, limit: int) -> list:
    chunk = []
    for i in range(limit):
        chunk.append(content[i::limit])
    return chunk


def ChunkIndex(content: str, limit: int) -> float:
    chunk = BuildChunk(content, limit)
    score = 0
    for i in range(len(chunk)):
        score = score + СomplIndex(chunk[i])
    return score / len(chunk)


def BuildKey(content: str, limit: int, letter: chr) -> str:
    chunk = BuildChunk(content, limit)
    key = ''
    for i in range(len(chunk)):
        key += grammar[(LetterToIndex[max(amount(chunk[i]), key=lambda x: chunk[i].count(x))] - LetterToIndex[letter]) % len(grammar)]
    return key


def prin(content: str, key: str):
    with open('key15.txt'.format(key), "w+", encoding="utf-8") as txt:
        txt.write(CipherText(content, key) + '\n' + str(СomplIndex(CipherText(content, key))))


def main():
    for i in range(1, len(grammar)):
        print(f'Limit of key >>> {i}, index for this chunk >>> {ChunkIndex(version8, i)}')
    print(BuildKey(version8, 20, "о"))
    # prin(my_file, Token['key15'])
    print(СomplIndex(my_file))
    # key = 'улановсеребряныепули'
    # prin(version8, key)


main()
