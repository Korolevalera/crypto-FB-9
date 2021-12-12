import os
#\/\/\/\/\/\/\/\/\/\|1 - Шифрування власного тексту ключами різної довжини|/\/\/\/\/\/\/\/\/\/#

chars = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
         'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

keys = ['со', 'мба', 'дива', 'нстол', 'дмизеволдизгонаролми']


def Char_filter(text):      # функція фільтрації тексту з лаби 1
    A = []
    text = text.lower()
    text = text.replace('ё', 'е')
    for ch in text:
        if ch in chars:
            A.append(ch)
    text = ''.join(A)
    return text


f = open(".\\going_to_the_river.txt", "r", encoding='UTF-8')
text = f.read()
f.close()

filtered_text = Char_filter(text)
f = open(".\\Filtered txt\\filtered.txt", "w")
f.write(filtered_text)
f.close()


def encode(text, key):      # функція шифрування
    A = []
    for i, ch in enumerate(text):
        # print(str(i) + "->" + ch)
        # індекс букви в алфавіті
        text_i = chars.index(ch)
        # багаторазовий прохід по буквам ключа
        key_i = chars.index(key[(i % len(key))])

        # зашифрований символ за формулою
        e_char = chars[(text_i + key_i) % len(chars)]

        # додаємо зашифровані символи в масив
        A.append(e_char)

    return ''.join(A)


def index_f(text):    # ф-я знаходження індексів відповідності
    index = 0
    for i in range(0, len(chars)):
        N = text.count(chars[i])
        index += N * (N - 1)
    index /= (len(text) * (len(text) - 1))
    return index


if os.path.exists(".\\task1-2.txt"):
    os.remove(".\\task1-2.txt")

# запис в файл індекса відкритого тексту
f = open(".\\task1-2.txt", "a")
s = "Normal text index: " + str(index_f(filtered_text)) + "\n\n"
f.write(s)

# цикл шифрування з різними ключами
# і підрахунку і. відповідності
for key in keys:
    e_text = encode(filtered_text, key)
    s = "Text, encrypted with key length " + \
        str(len(key)) + " index = " + \
        str(index_f(e_text)) + "\n" + e_text + "\n\n"
    f.write(s)
f.close()

#\/\/\/\/\/\/\/\/\/\|3 - Розшифровування шифротексту|/\/\/\/\/\/\/\/\/\/#
f = open(".\\v5_cypher.txt", "r", encoding='UTF-8')
e_text = f.read()
e_text = e_text.replace('\n', '')
f.close()


def find_key(text):  # ф-я знаходження довжини ключа
    # розділeння на частини з різним кроком
    parts = []
    average_index = 0
    for i in range(2, len(chars)):
        for q in range(0, i):
            parts.append(text[q::i])
        # підрахунок середнього значення індексу для кожного періоду
            average_index += index_f(parts[-1])
        average_index /= i
        s = "r" + "(" + str(i) + ")" + ": " + str(average_index) + "\n"
        f.write(s)
        average_index = 0

    # за результатами експерименту
    # довжина ключа: 16
    # так як значення індексу тут
    # найбільш наближене до теоритичного
    # (0.0553)

    # повторне отримання частин тексту розділених з періодом 16
    parts = []
    for i in range(16):
        parts.append(text[i::16])

    # підрахунок букв які зустрічаються в отриманих частинах найчастіше
    A = []
    freq = []
    max_freq_letters = []
    for i in range(len(parts)):
        # створення масива з елемента масива
        for char in parts[i]:
            A.append(char)
        # підрахунок
        for ch in A:
            freq.append(A.count(ch) / len(A))
        max_freq = max(freq)
        #print(A[freq.index(max_freq)] + ": " + str(max_freq))
        max_freq_letters.append(A[freq.index(max_freq)])
        A = []
        freq = []

    # знаходження ключа шифром цезаря з k = 14(о)
    key = []
    for ch in max_freq_letters:
        key.append(chars[(chars.index(ch) - 14) % len(chars)])
    print(key)  # делолисоборотней <-- декелисоборойдей
    return ''.join(key)


def decode(text, key):  # ф-я розшифрування
    A = []
    for i, ch in enumerate(text):
        text_i = chars.index(ch)
        key_i = chars.index(key[(i % len(key))])
        e_char = chars[(text_i - key_i) % len(chars)]
        A.append(e_char)
    return ''.join(A)


if os.path.exists(".\\average_indexes.txt"):
    os.remove(".\\average_indexes.txt")
f = open(".\\average_indexes.txt", "a")
# виклик знаходження ключа
find_key(e_text)
f.close()

# тут методом перебору ми замінювали деякі букви отриманого ключа
# для отримання коректного результату
print("Enter key to decode text:")
key = input()
d_text = decode(e_text, key)
# запис отриманого відкритого тексту в файл
f = open(".\\v5_text.txt", "w")
f.write(d_text)
f.close()
