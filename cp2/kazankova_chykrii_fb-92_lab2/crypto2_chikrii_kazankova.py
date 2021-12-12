###
#Лабораторная работа №2 - Шифр Вижинера, авторство: Чикрий К.К. (ФБ-92), Казанкова М.Е. (ФБ-92)
###


from viginereCipher import *


def readFile(filePath):
    with open(filePath, 'r', encoding = 'utf-8') as file:
        return file.read()


#Задание 1 и 2
#Самостоятельно был подобран текст из текстового файла gogol.txt
print("Task 1")
textToAnalyze = readFile("gogol.txt")
textToAnalyze = prepareText(textToAnalyze)
keyChain = ["аб", "абв", "абвг", "абвгд", "абвгдежзийкл"]
encryptedTexts = []
for key in keyChain:
    encryptedTexts.append(encrypt(key, textToAnalyze))
#print("Encrypted this text:\n" + textToAnalyze + "\nWith this keys:" + str(keyChain))
i = 0
#while i < len(encryptedTexts):
    #print("As a result of encryption with key  \"" + keyChain[i] + "\" we have this text with hit index " + str(getHitIndex(encryptedTexts[i])) + ":" + encryptedTexts[i])
    #i += 1

#Задание 3
#Зашифрованный текст сохранен в файле var7.txt
print("Task 2")
textToAnalyze = readFile("var7.txt")
print(decryptWithoutKey(textToAnalyze))
# f = open('var7.txt', 'r')
# textToAnalyze = f.read()
# textToAnalyze = prepareText(textToAnalyze)
# f.close()
# print("Key len -",getKeyLen(textToAnalyze))
# print(decryptWithoutKey(textToAnalyze))