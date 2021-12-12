###
#Лабораторная работа №1, авторство: Чикрий К.К. (ФБ-92), Казанкова М.Е. (ФБ-92)
###


import math
from nltk import everygrams
from collections import Counter
import re


alphabet = ''.join([chr(i) for i in range(ord('а'),ord('а')+32)])


def bubbleSortTuplesBySecondElement(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j][1] < arr[j + 1][1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def openClearText(filePath, clearSpaces=False):
    
    #Открываем файл через with open
    text = ""
    with open(filePath, 'r', encoding = 'utf-8') as file:
        text = file.read()

    #Выкидываем из текста все лишние символы, и делаем заглавные буквы строчными
    text = text.lower()
    if clearSpaces:
        text = text.replace(' ', '')
    else:
        #Два раза, что бы осталось не более одного пробела в ряд если изначально их было > 2
        text = text.replace('  ',' ')
        text = text.replace('  ',' ')
    chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', ',', '?', '!', ':', ';', '/', '\\', '(', ')', '\"', '\'', '\n', '-', '_', '—', '“', '„', '…', '[', ']', '«', '»', ' ']
    for char in chars:
        text = text.replace(char, '')
    #Заменяем ё на е и ъ на ь
    text = text.replace('ё', 'е')
    text = text.replace('ъ', 'ь')


    #Возвращаем строкой
    return text


#Запись в файл через with open
def writeFile(filePath, text):
    with open(filePath, 'w') as file:
        file.write(text)


#Абсолютная частота
def getAbsoluteFrequency(text):
    return Counter(text).most_common()


#Относительная частота
def getRelativeFrequency(text):
    relativeFreq = []
    absFreq = getAbsoluteFrequency(text)
    for char in absFreq:
        currTuple = ((char[0]), (int(char[1])/len(text)))
        relativeFreq.append(currTuple)
    return relativeFreq


#Энтропия
def getEntropyMono(text):
    relFreq = []
    n = 1
    relFreq = getRelativeFrequency(text)
    entropy = 0
    for char in relFreq:
        entropy += -char[1] * math.log2(char[1])
    entropy *= 1/n
    return entropy


#Избыточность монограмм
def getH1(text, spaces=False):
    n = 0
    if spaces:
        n = 32
    else:
        n = 31
    return 1 - getEntropyMono(text) / math.log2(n)


def countBigramAbsFreqWithInter(text):
    allSymbols = list(set(text))
    #print(allSymbols)
    i = 0
    allPossibleBigrams = []
    while (i < len(allSymbols)):
        y = 0
        while(y < len(allSymbols)):
            allPossibleBigrams.append(allSymbols[i] + allSymbols[y])
            y += 1
        i += 1
    #print(allPossibleBigrams)
    output = []
    for bigram in allPossibleBigrams:
        i = 0
        bigramFreq = 0 
        while(i < len(text) - 1):
            if text[i] + text[i+1] == bigram:
                bigramFreq += 1
            i += 1
        output.append((bigram, bigramFreq))
        #Clear bigrams with 0 freq
        bigramsToDelete = []
        for bigram in output:
            if bigram[1] == 0:
                bigramsToDelete.append(bigram)
        for bigram in bigramsToDelete:
            output.remove(bigram)
    return bubbleSortTuplesBySecondElement(output)


def getRelativeFrequencyBigramsWithInter(text):
    relativeFreq = []
    absFreq = countBigramAbsFreqWithInter(text)
    ##print("Len for bigrams with inter:", int(len(text)/2 + 0.5))
    length = len(text) - 1
    for chars in absFreq:
        currTuple = ((chars[0]), (int(chars[1])/length))
        relativeFreq.append(currTuple)
    return relativeFreq

                
def getEntropyBigramsWithInter(text):
    relFreq = []
    n = 2
    relFreq = getRelativeFrequencyBigramsWithInter(text)
    entropy = 0
    for char in relFreq:
        entropy += -char[1] * math.log2(char[1])
    entropy *= 1/n
    return entropy


def getH2WithIntersect(text, spaces=False):
    n = 0
    if spaces:
        n = 32
    else:
        n = 31
    return 1 - getEntropyBigramsWithInter(text) / math.log2(n)


def countBigramAbsFreqWithoutInter(text):
    allSymbols = list(set(text))
    #print(allSymbols)
    i = 0
    allPossibleBigrams = []
    while (i < len(allSymbols)):
        y = 0
        while(y < len(allSymbols)):
            allPossibleBigrams.append(allSymbols[i] + allSymbols[y])
            y += 1
        i += 1
    #print(allPossibleBigrams)
    output = []
    for bigram in allPossibleBigrams:
        i = 0
        bigramFreq = 0 
        while(i < len(text) - 1):
            if text[i] + text[i+1] == bigram:
                bigramFreq += 1
            i += 2
        output.append((bigram, bigramFreq))
        #Clear bigrams with 0 freq
        bigramsToDelete = []
        for bigram in output:
            if bigram[1] == 0:
                bigramsToDelete.append(bigram)
        for bigram in bigramsToDelete:
            output.remove(bigram)
    return bubbleSortTuplesBySecondElement(output)


def getRelativeFrequencyBigramsWithoutInter(text):
    relativeFreq = []
    absFreq = countBigramAbsFreqWithoutInter(text)
    ##print("Len for bigrams with inter:", int(len(text)/2 + 0.5))
    length = 0
    if len(text) %2 == 0:
        length = len(text)/2
    else:
        length = (len(text) - 1)/2
    for chars in absFreq:
        currTuple = ((chars[0]), (int(chars[1])/length))
        relativeFreq.append(currTuple)
    return relativeFreq

def getEntropyBigramsWithoutInter(text):
    relFreq = []
    n = 2
    relFreq = getRelativeFrequencyBigramsWithoutInter(text)
    entropy = 0
    for char in relFreq:
        entropy += -char[1] * math.log2(char[1])
    entropy *= 1/n
    return entropy

def getH2WithoutIntersect(text, spaces=False):
    n = 0
    if spaces:
        n = 32
    else:
        n = 31
    return 1 - getEntropyBigramsWithoutInter(text) / math.log2(n)


print("Welcome to laba 1!")
path = input("Enter file path:")
textToAnalyze = openClearText(path, clearSpaces=False)
print("Analyzing")
outputString = ""
outputString += "With spaces:\nMono\nrelative freq:\n"
for mono in getRelativeFrequency(textToAnalyze):
    outputString += mono[0] + "\t" + str(mono[1]) + "\n"
outputString += "Entropy: " + str(getEntropyMono(textToAnalyze)) + '\n'
outputString += "H1: " + str(getH1(textToAnalyze)) + '\n'
outputString += "Bigrams with intersection:\nRel freq:\n"
for bi in getRelativeFrequencyBigramsWithInter(textToAnalyze):
    outputString += bi[0] + "\t" + str(bi[1]) + "\n"
outputString += "Entropy: " + str(getEntropyBigramsWithInter(textToAnalyze)) + '\n'
outputString += "H2: " + str(getH2WithIntersect(textToAnalyze)) + '\n'
outputString += "Bigrams without intersection:\nRel freq:\n"
for bi in getRelativeFrequencyBigramsWithoutInter(textToAnalyze):
    outputString += bi[0] + "\t" + str(bi[1]) + "\n"
outputString += "Entropy: " + str(getEntropyBigramsWithoutInter(textToAnalyze)) + '\n'
outputString += "H2: " + str(getH2WithoutIntersect(textToAnalyze)) + '\n'

textToAnalyze = openClearText(path, clearSpaces=True)

outputString += "Without spaces:\nMono\nrelative freq:\n"
for mono in getRelativeFrequency(textToAnalyze):
    outputString += mono[0] + "\t" + str(mono[1]) + "\n"
outputString += "Entropy: " + str(getEntropyMono(textToAnalyze)) + '\n'
outputString += "H1: " + str(getH1(textToAnalyze)) + '\n'
outputString += "Bigrams with intersection:\nRel freq:\n"
for bi in getRelativeFrequencyBigramsWithInter(textToAnalyze):
    outputString += bi[0] + "\t" + str(bi[1]) + "\n"
outputString += "Entropy: " + str(getEntropyBigramsWithInter(textToAnalyze)) + '\n'
outputString += "H2: " + str(getH2WithIntersect(textToAnalyze)) + '\n'
outputString += "Bigrams without intersection:\nRel freq:\n"
for bi in getRelativeFrequencyBigramsWithoutInter(textToAnalyze):
    outputString += bi[0] + "\t" + str(bi[1]) + "\n"
outputString += "Entropy: " + str(getEntropyBigramsWithoutInter(textToAnalyze)) + '\n'
outputString += "H2: " + str(getH2WithoutIntersect(textToAnalyze)) + '\n'

print("Done, output in out.txt file")
writeFile("out.txt", outputString)