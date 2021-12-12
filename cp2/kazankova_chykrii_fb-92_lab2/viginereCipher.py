###
#Лабораторная работа №2 - Шифр Вижинера, авторство: Чикрий К.К. (ФБ-92), Казанкова М.Е. (ФБ-92)
###


def getDict():
    #Русский алфавит, только строчные символы
    return [chr(i) for i in range(ord('а'),ord('а')+32)]


def prepareText(text):
    preparedText = text.lower()
    preparedText = preparedText.replace('ё', 'е')
    #Удалить лишние символы
    lettersToDelete = []
    for letter in preparedText:
        try:
            getDict().index(letter)
        except ValueError:
            lettersToDelete.append(letter)
    for letterToDelete in lettersToDelete:
        preparedText = preparedText.replace(letterToDelete, '')
    return preparedText


def prepareKey(key, length):
    preparedKey = prepareText(key)
    if len(preparedKey) == length:
        return preparedKey
    elif len(preparedKey) > length:
        return preparedKey[0:length]
    else:
        unprepKey = preparedKey
        while len(preparedKey) < (length - len(unprepKey) + 1):
            preparedKey += unprepKey
        if len(preparedKey) != length:
            preparedKey += unprepKey[0:(length - len(preparedKey))]
        return preparedKey


def encode(text):
    encoded = []
    for i in text:
        encoded.append(getDict().index(i))
    #print(encoded)
    return encoded


def decode(encodedText):
    alphabet = getDict()
    decoded = []
    for i in encodedText:
        decoded.append(alphabet[i])
    #print(decoded)
    return ''.join(decoded)


def encrypt(key, text):
    encodedText = encode(prepareText(text))
    encodedKey = encode(prepareKey(key, len(encodedText)))
    encodedEncryptedText = []
    i = 0
    while i < len(text):
        encodedEncryptedText.append((encodedKey[i] + encodedText[i])%len(getDict()))
        i += 1
    return decode(encodedEncryptedText)


def decrypt(key, encText):
    key = prepareKey(key, len(encText))
    encodedKey = encode(key)
    encodedText = encode(encText)
    encodedDecryptedText = []
    i = 0
    while i < len(encText):
        encodedDecryptedText.append((encodedText[i] - encodedKey[i] + len(getDict()))%len(getDict()))
        i += 1
    return decode(encodedDecryptedText)


def bubbleSortTuplesBySecondElement(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j][1] < arr[j + 1][1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                
    return arr


def getKeyLen(encText):
    i = 1
    maxKeySize = 31
    matchAnalysResults = []
    while i < maxKeySize and i < (len(encText) - 1)/2:
        analyzedStr1 = encText[i:]
        analyzedStr2 = encText[0:len(analyzedStr1)]
        #print("str1:" + analyzedStr1[:10])
        #print("str2:" + analyzedStr2[:10])
        matches = 0
        y = 0
        while y < len(analyzedStr1):
            if analyzedStr1[y] == analyzedStr2[y]:
                matches += 1
            y += 1
        matchAnalysResults.append((i, matches))
        i += 1
    matchAnalysResults = bubbleSortTuplesBySecondElement(matchAnalysResults)
    preMaxIndex = matchAnalysResults[1][1]
    possibleKeyLength = []
    for keyLenAnalysTuple in matchAnalysResults:
        if keyLenAnalysTuple[1] == preMaxIndex:
            possibleKeyLength.append(keyLenAnalysTuple[0])
    possibleKeyLength.sort()
    #print(possibleKeyLength)
    print("Indexes while searching key length:\n", matchAnalysResults)
    return possibleKeyLength[0]


def sliceToBlocks(encText):
    keyLen = getKeyLen(encText)
    
    i = 0
    blocks = []
    while i < keyLen:
        block = encText[i::keyLen]
        blocks.append(block)
        i += 1
    return blocks


def decryptWithoutKey(encText):
    encText = prepareText(encText)
    mostCommonLetter = 'о'
    blocks = sliceToBlocks(encText)
    key = ""
    for block in blocks:
        absFreqs = []
        for letter in getDict():
            absFreqs.append(block.count(letter))
        mostFreqEncLetterDictIndex = absFreqs.index(max(absFreqs))
        keyLetterIndex = mostFreqEncLetterDictIndex - getDict().index(mostCommonLetter)
        keyLetterIndex = keyLetterIndex % len(getDict())
        key += decode([keyLetterIndex])
    print("Key length was -", getKeyLen(encText))
    print("The key was -", key)
    
    return decrypt(key, encText)


def getHitIndex(strng):
    if len(strng) == 0:
        return 0

    strng = prepareText(strng)

    hitIndex = 0.0

    for letter in getDict():
        Quantity = 0
        for strLetter in strng:
            if strLetter == letter:
                Quantity += 1
        try:
            hitIndex  += (Quantity*(Quantity - 1))/(len(strng)*(len(strng) - 1))
        except Exception:
            return 0
    print (hitIndex)
    return hitIndex


def demo():
    print("Welcome to lab2!")
    text = prepareText(input("text:"))
    key = prepareKey(input("key:"), len(text))
    print("Encrypted:\t", encrypt(key, text), "\nDecrypted:\t", decrypt(key, encrypt(key, text)))