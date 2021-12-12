import operator
from collections import Counter
from itertools import permutations




def openfile(t):
    with open(t, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    return text
text = openfile('V4')
text = text.replace('\n', '')

def euclid(a, b):
    if b == 0:  
        return a, 1, 0
    else:
        d, x, y = euclid(b, a % b)
        return d, y, x - y * (a // b)
    
def linear(a, b, m):
  gcd, a1, y = euclid(a, m)
  answers = []
  if gcd == 1 :
    if ((a*a1)%m) == 1:
      answers.append((a1*b)%m)
      return answers
  else:
    if b% gcd != 0:
      return None
    else:
      gcd, q, a1 =euclid(a,m)
      for i in range (gcd-1):
        x = (a1*b)%m + i*m
        answers.append(x)
      return answers
  
def count_bigrams(text):
    bigram = []
    frequent = []
    bigram = [text[i: i + 2] for i in range(0, (len(text)), 2)]
    count = Counter(bigram)
    frequentBigrams = sorted(count.items(), key = operator.itemgetter(1), reverse=True)
    for i in frequentBigrams[:5]: frequent.append(i[0])
    return frequent

def permutation(frequent, rusBigrams):
   possible = permutations(frequent)
   result = []
   for p in possible:
        combinations = {}
        for i in range(len(rusBigrams)):
            combinations[rusBigrams[i]] = p[i]
        result.append(combinations) 
   return result
    
def countIndex(bigram):  
  res1 = alphabet.index(bigram[0])*(len(alphabet))
  res2 = alphabet.index(bigram[1])
  res = res1 + res2
  return res

def xAndY():
  Xs = []
  for i in rusBigrams:
    Xs.append(countIndex(i))
  Ys = []
  for i in frequent:
    Ys.append(countIndex(i))  
  return Xs, Ys

def find_key(pair):  
  y1, x1 = pair[0][0], pair[0][1]  
  y2, x2 = pair[1][0], pair[1][1]
  a = linear(x1-x2, y1-y2,len(alphabet)**2)
  b = []
  if a != None:
    for el in range(len(a)):
     b.append((y1-(x1*a[el]))%len(alphabet)**2)      
    return (a[0], b[0])

def decrypter(a, b, m, text):
  decryptedText = []
  gcd, a1, q =euclid(a,m)
  lentext = len(text)
  if lentext%2==1: lentext-=1
  for bi in [text[i: i + 2] for i in range(0, lentext, 2)]:
     y = countIndex(bi)
     x = (y-b)*a1%m
     x2 = x%31 
     x1 = ((x-x2)//31)%31
     x1_letter = alphabet[x1]
     x2_letter = alphabet[x2]
     if nonExistBigramsCheck(x1_letter, x2_letter)==False: 
       if a!=0: 
         decryptedText.append(x1_letter+x2_letter)
     else:
       decryptedText.clear()
       return rightKeys, decryptedText
    
  if len(decryptedText) > 0:
    decryptedText = ''.join(decryptedText)
    rightKeys.append((a,b))
  return rightKeys, decryptedText
  
def nonExistBigramsCheck(let1,let2):
  nonExist = ('аь', 'еь', 'жы', 'уь', 'фщ', 'хы', 'хь', 'цщ', 'цю', 'чф', 'чц', 'чщ', 'шы', 'щъ', 'щы', 'ыь', 'ьы', 'эы', 'эь', 'юы', 'юь', 'яы', 'яь', 'ьь')
  if let1+let2 in nonExist:
    return True
  else: return False

frequent = count_bigrams(text)
rusBigrams = ['ст', 'но', 'то', 'на', 'ен']
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

keys = []
rightKeys = []
allpairs = []
ans = []

Xs, Ys = xAndY()
pairs = permutation(Xs, Ys) 

for i in range(len(pairs)):     
    for x, y in pairs[i].items(): 
         allpairs.append((x, y))
allpairs = list(set(allpairs))

allpairs = list(permutations(allpairs, 2))

for i in range(len(allpairs)):
  ans = (find_key(allpairs[i]))
  if not ans in keys and ans!=None:
    keys.append(ans)
for key in keys:
  rightKeys, decryptedText = decrypter(key[0], key[1], 961, text)
  if len(decryptedText)>0:
   with open('txt.txt', 'w', encoding='utf-8') as file:
        file.write(decryptedText)
        file.write('\n')
  
print(rightKeys)

del keys, allpairs, ans
