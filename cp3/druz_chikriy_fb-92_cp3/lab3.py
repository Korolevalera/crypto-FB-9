from array import *
import math
from collections import Counter
from progress.bar import IncrementalBar

alphavit = "абвгдежзийклмнопрстуфхцчшщъыэюя"
m = len(alphavit)


# Очистка файла
def clearText(text):
    clear_text = (
        text.replace("\n", " ")
        .replace("\r", "")
        .lower()
        .replace("ё", "е")
        .replace("ь", "ъ")
        .replace(" ", "")
    )
    for char in clear_text[:]:
        if char not in alphavit:
            clear_text = clear_text.replace(char, "")
    # fout = open(name + "_clear.txt", "w", encoding="utf-8")
    # fout.close()
    return clear_text


# Частота букв
def letter_frequency_in_text(text):
    counts = Counter(text)
    for i in sorted(counts, key=counts.get, reverse=True):
        print(i, counts[i] / len(text))


def relFreqForChar(text, char):
    # print(text)
    return text.count(char)


# Частота биграмм
def bigramm_frequencey(text):
    bigramms = []
    i = 0
    if len(text) % 2 == 1:
        while i < len(text) - 2:
            bigramms.append((text[i], text[i + 1]))
            i += 2
        # bigramms = [(text[i], text[i + 1]) for i in range(1, len(text) - 2, 2)]
    else:
        while i < len(text) - 1:
            bigramms.append((text[i], text[i + 1]))
            i += 2
        # bigramms = [(text[i], text[i + 1]) for i in range(1, len(text) - 1, 2)]
    # counts = Counter(bigramms)
    # for i in sorted(counts, key=counts.get, reverse = True):
    #     print(i,counts[i]/len(bigramms))
    return bigramms


# Энтропия и излишек языка для монограмм
def entrophy_for_letters(text):
    counts = Counter(text)
    entropy = 0
    for i in counts.values():
        entropy += -(i / len(text)) * math.log2(i / len(text))
    print("Entropy H1 without spaces: " + str(entropy))
    print("Surplus H1 without spaces: " + str(1 - entropy / math.log2(31)))


# Энтропия и излишек языка для биграмм
def entrophy_for_bigramms(text):
    bigramms = {}
    if len(text) % 2 == 1:
        bigramms = [(text[i - 1], text[i]) for i in range(1, len(text) - 1, 2)]
    else:
        bigramms = [(text[i - 1], text[i]) for i in range(1, len(text), 2)]
    counts = Counter(bigramms)
    entropy = 0
    for i in counts.values():
        entropy += -(i / len(bigramms)) * math.log2(i / len(bigramms))
    entropy = entropy / 2
    print("Entropy H2 without spaces without intersection: " + str(entropy))
    print(
        "Surplus H2 without spaces without intersection: "
        + str(1 - entropy / math.log2(31))
    )


def gcd(a, b, u0=1, v0=0, u1=0, v1=1):
    result = []
    r1 = 0
    r2 = 0
    if a >= b:
        r1 = a
        r2 = b
    else:
        r1 = b
        r2 = a
    if r2 == 0:
        return [0, 0, 0]
    r3 = int(r1 % r2)
    q = int(r1 / r2)
    u3 = u0 - q * u1
    v3 = v0 - q * v1
    if r3 == 0:
        return (r2, u1, v1)
    result = gcd(r2, r3, u0=u1, v0=v1, u1=u3, v1=v3)
    if a > b:
        return result
    else:
        return (result[0], result[2], result[1])


def line_comparison(a, b):
    result = []
    res = gcd(a, math.pow(m, 2))
    if res[0] == 1:
        result.append(int((b * res[1]) % pow(m, 2)))
        return result
    elif res[0] > 1:
        if int(b % res[0]) != 0:
            return 0
        else:
            i = 0
            while i < res[0]:
                result.append(
                    int(
                        (
                            (b / res[0])
                            * gcd(a / res[0], math.pow(m, 2) / res[0], 1, 0, 0, 1)[1]
                        )
                        % (pow(m, 2) / res[0])
                    )
                    + int(i * (pow(m, 2) / res[0]))
                )
                i += 1
            return result
    else:
        # print("Error")
        return 0


def birgramm(a, b):
    return int((a * m + b) % pow(m, 2))


i = 0
bigramm_alphavit = []
while i < m:
    j = 0
    while j < m:
        bigramm_alphavit.append(((alphavit[i], alphavit[j]), birgramm(i, j)))
        j += 1
    i += 1


def getKeys(XX_YY):
    keys = []
    for xx_yy in XX_YY:
        a = line_comparison(
            int(xx_yy[0][0] - xx_yy[0][1]) % pow(m, 2),
            int(xx_yy[1][0] - xx_yy[1][1]) % pow(m, 2),
        )
        if a == 0:
            pass
        elif len(a) == 1:
            a[0] = a[0] % pow(m, 2)
            b = int(xx_yy[1][0] - (a[0] * xx_yy[0][0]))
            b = b % pow(m, 2)
            keys.append((a[0], b))
        else:
            i = 0
            while i < len(a):
                a[i] = a[i] % pow(m, 2)
                b = int(xx_yy[1][0] - (a[i] * xx_yy[0][0]))
                b = b % pow(m, 2)
                keys.append((a[i], b))
                i += 1
    return list(set(keys))


def encode_bigramm(bigr, a, b):
    en_bigr = int(a * bigr + b) % pow(m, 2)
    return en_bigr


def encode_text(text, a, b):
    en_text = ""
    en_bigr = []
    bigramms = bigramm_frequencey(text)
    for bigr in bigramms:
        i = 0
        while i < len(bigramm_alphavit):
            if bigr == bigramm_alphavit[i][0]:
                en_bigr.append(encode_bigramm(bigramm_alphavit[i][1], a, b))
            i += 1
    for bigr_code in en_bigr:
        i = 0
        while i < len(bigramm_alphavit):
            if bigr_code == bigramm_alphavit[i][1]:
                en_text = en_text + str(bigramm_alphavit[i][0][0])
                en_text = en_text + str(bigramm_alphavit[i][0][1])
            i += 1
    return en_text


def decode_bigramm(bigr, a, b):
    de_bigr = []
    res = line_comparison(a, (bigr - b) % pow(m, 2))
    if res == 0:
        return
    elif len(res) == 1:
        de_bigr.append(int(res[0]) % pow(m, 2))
    else:
        i = 0
        while i < len(res):
            de_bigr.append(int(res[i]) % pow(m, 2))
            i += 1
    return de_bigr


def decode_text(text, a, b):
    de_text = ""
    de_bigr = []
    bigramms = bigramm_frequencey(text)
    for bigr in bigramms:
        i = 0
        while i < len(bigramm_alphavit):
            if bigr == bigramm_alphavit[i][0]:
                de_bigr.append(decode_bigramm(bigramm_alphavit[i][1], a, b))
            i += 1
    # print(de_bigr)
    for bigr_code in de_bigr:
        if bigr_code == None:
            return "ыыыыыыыыыыыыыыы"
        elif len(bigr_code) == 1:
            i = 0
            while i < len(bigramm_alphavit):
                if bigr_code[0] == bigramm_alphavit[i][1]:
                    de_text += str(bigramm_alphavit[i][0][0])
                    de_text += str(bigramm_alphavit[i][0][1])
                i += 1
        else:
            bigr_bigr = []
            i = 0
            while i < len(bigr_code):
                j = 0
                while j < len(bigramm_alphavit):
                    if bigr_code[i] == bigramm_alphavit[j][1]:
                        bigr_bigr.append(bigramm_alphavit[j][0])
                    j += 1
                i += 1
            de_text += str(bigr_bigr)
    return de_text


def main():
    filename = "var6"
    # filename = "A_ja_kto_clear"
    fin = open(filename + ".txt", "r", encoding="utf-8")
    filetext = fin.read()
    fin.close()
    filetext = clearText(filetext)
    bigramms = bigramm_frequencey(filetext)

    count = sorted(Counter(bigramms), key=Counter(bigramms).get, reverse=True)
    # print(count)
    frequent_bigrams_ct = []
    j = 0
    for i in count:
        if j != 5:
            frequent_bigrams_ct.append(i)
            j += 1
        else:
            break
    # print(frequent_bigrams_ct)
    frequent_bigrams_pt = [
        (("с", "т"), birgramm(17, 18)),
        (("н", "о"), birgramm(13, 14)),
        (("т", "о"), birgramm(18, 14)),
        (("н", "а"), birgramm(13, 0)),
        (("е", "н"), birgramm(5, 13)),
    ]
    # print(frequent_bigrams_pt)
    i = 0
    a = []
    b = []
    while i < len(frequent_bigrams_ct):
        j = 0
        while j < m:
            if alphavit[j] == frequent_bigrams_ct[i][0]:
                a.append(j)
            if alphavit[j] == frequent_bigrams_ct[i][1]:
                b.append(j)
            j += 1
        i += 1
    Y = []
    i = 0
    while i < len(frequent_bigrams_ct):
        Y.append((frequent_bigrams_ct[i], birgramm(a[i], b[i])))
        i += 1
    # print(X)
    X_Y = []
    i = 0
    while i < 5:
        j = 0
        while j < 5:
            X_Y.append((frequent_bigrams_pt[i][1], Y[j][1]))
            j += 1
        i += 1
    # print(X_Y)
    X = frequent_bigrams_pt
    # print("X:", X)
    X_X = []
    i = 0
    # y = 0
    while i < len(X):
        y = 0
        while y < len(X):
            # if i < y:
            X_X.append((X[i][1], X[y][1]))
            y += 1
        i += 1
    # print("X_X:", X_X)
    # print("Y:", Y)
    Y_Y = []
    i = 0
    # y = 0
    while i < len(Y):
        y = 0
        while y < len(Y):
            # if i < y:
            Y_Y.append((Y[i][1], Y[y][1]))
            y += 1
        i += 1
    # print("Y_Y:", Y_Y)
    XX_YY = []
    i = 0
    # y = 0
    while i < len(X_X):
        y = 0
        while y < len(Y_Y):
            XX_YY.append((X_X[i], Y_Y[y]))
            y += 1
        i += 1
    # print("XX_YY:", XX_YY)
    keys = getKeys(XX_YY)

    i = 0
    bar = IncrementalBar("Decrypting:", max=len(keys))
    decryptedTexts = []
    while i < len(keys):
        de_text = decode_text(filetext, keys[i][0], keys[i][1])
        decryptedTexts.append(((keys[i][0], keys[i][1]), de_text))
        bar.next()
        i += 1
    bar.finish()
    # print(decryptedTexts)
    mostCommon = ["о", "а"]
    # print(decode_text(filetext, 324, 112))
    i = 0
    possibleRightOptions = []
    while i < len(decryptedTexts):
        possibleRightOptions.append(
            (
                relFreqForChar(decryptedTexts[i][1], "о"),
                relFreqForChar(decryptedTexts[i][1], "а"),
                i,
            )
        )
        i += 1
    # print(possibleRightOptions)
    possibleRightOptions.sort(reverse=True)

    a = possibleRightOptions[0][0]
    b = possibleRightOptions[0][1]
    i = 0
    while i < len(possibleRightOptions) and i < 1:
        print(
            "A = "
            + str(decryptedTexts[possibleRightOptions[i][2]][0][0])
            + "\nB = "
            + str(decryptedTexts[possibleRightOptions[i][2]][0][1])
            + "\nText:\n"
            + str(decryptedTexts[possibleRightOptions[i][2]][1])
        )
        i += 1


main()
