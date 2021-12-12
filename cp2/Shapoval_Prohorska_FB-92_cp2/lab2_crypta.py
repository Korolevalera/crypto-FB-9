# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 10:12:50 2021

@author: olya

"""
import random
import re
from collections import Counter

with open('text.txt','r',encoding='utf-8') as file:
    text = file.read()
with open('shifrtext.txt', 'r',encoding='utf-8') as file:
    shifrtext = file.read()
shifrtext = re.sub("[^А-Яа-я]", "", shifrtext)
shifrtext = shifrtext.replace('\n', '')
with open('shifrtext.txt', 'w', encoding='utf-8') as file:
        file.write(shifrtext)
    
  
def alphabet():
    a = ord('а')
    alphabet =''.join([chr(i) for i in range(a,a+32)])
    #print(alphabet)
    return alphabet
    
alphabet = alphabet()

def randomKeys():
    keys = []

    for i in range(2, 6):
        rand_string = ''.join(random.choice(alphabet) for al in range(i))
        keys.append(rand_string)
    for i in range(10, 21):
        rand_string = ''.join(random.choice(alphabet) for al in range(i))
        keys.append(rand_string)
    #print(keys) 
    return keys
    
keys = randomKeys()   

def encode(key, text):
    encryptedtext = []
    for i in range(len(text)):
       encryptedtext.append( alphabet[(alphabet.index(text[i]) + alphabet.index(key[i % len(key)]))% len(alphabet)])
    secrettext = ''.join(encryptedtext[i] for i in range(len(encryptedtext)))
    #print(secrettext)
    with open('secrettext.txt','w',encoding='utf-8') as file:
       file.write(secrettext)
    return secrettext

#encryptedtext = encode(keys[10], text)  

def decode(key, secrettext):
    decryptedtext = []
    for i in range(len(secrettext)):
        decryptedtext.append( alphabet[(alphabet.index(secrettext[i]) - alphabet.index(key[i % len(key)]) % len(alphabet))])
    text = ''.join(decryptedtext[i] for i in range(len(decryptedtext)))
    #print(text) 
    return text
#decode(keys[10], encryptedtext)
      
def index(text):
    d = Counter(text)
    #print(d)
    ind = 0
    for i in d:
        ind += d[i] * (d[i] - 1)
    ind /= (len(text) * (len(text) - 1))
    return ind
index(text)

def countindex():
    ind = {}
    for i in range(15):
        encryptedtext = encode(keys[i], text)
        ind[len(keys[i])] = index(encryptedtext)
    #print(ind)
    return ind

countindex()

def makeBlocks(text, leng):              
    blocks = []
    for i in range(leng):
        blocks.append(text[i::leng])
    #print(blocks)
    return blocks 

def findlenkey():
    inddic = {}
    for i in range (1,31):
        block = makeBlocks(shifrtext, i)
        indexx = 0
        for bl in block:
            indexx += index(bl)
        indexx /= i
        inddic[i] = indexx
    #print(inddic)    
    return inddic   
    
def SecretKey(len_key):
    block = makeBlocks(shifrtext, len_key) 
    letters = "оеа"
    for l in letters:
        ourkey =""
        for bl in block:
            countblock = Counter(bl[i] for i in range(len(bl)))
            maxcount = max(countblock, key=countblock.get)
            ourkey+=alphabet[(alphabet.index(maxcount)-alphabet.index(l))%len(alphabet)]
        print(ourkey)


len_of_key = max(findlenkey(), key=findlenkey().get)
SecretKey(len_of_key)
#keeey = 'громнкавьдума'
#firsttext = decode(keeey, shifrtext)
#keeey2 = 'громнкаведьма'
#firsttext = decode(keeey2, shifrtext)
#with open('firsttext.txt', 'w', encoding='utf-8') as file:
        #file.write(firsttext)
finalkey = 'громыковедьма'
finaltext = decode(finalkey, shifrtext)
with open('finaltext.txt', 'w', encoding='utf-8') as file:
        file.write(finaltext)












    
    
    
    
   