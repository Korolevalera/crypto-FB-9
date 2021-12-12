from collections import Counter
from itertools import permutations, combinations
ABC = 'абвгдежзийклмнопрстуфхцчшщьыэюя' # алфавіт
PB = ['ст', 'но', 'то', 'на', 'ен'] # популярні біграми
MOD = len(ABC)**2

big_to_val = lambda bigram: (ABC.find(bigram[0])*len(ABC) + ABC.find(bigram[1])) % (len(ABC)**2) # біграма в числове значення
val_to_big = lambda value: (ABC[value//len(ABC)]) + (ABC[value%len(ABC)]) # числове значення в біграму

def egcd(a, b): # пошук найбільшого спільного кратного
    if(b==0):
        return a
    else:
        return egcd(b, a % b)

def crt_bigrams(text): # створення біграм 
    bigrams = []
    i = 0
    while i < len(text)-1:
        bigrams.append(text[i] + text[i+1])
        i += 2
    return bigrams

def get_popular_big(bigrams, length): # визначення найпопулярнишіх біграм
    buf = bigrams.copy()
    lst = []
    for i in range(length):
        lst.append(max(buf, key=buf.get))
        buf.pop(lst[-1])
    return lst

def get_permutations(lst1, lst2): # створення перестановок  
    result = []
    perms = permutations(lst2) 
    for row in perms:
        dct = {}
        for i in range(len(lst1)):
            dct[lst1[i]] = row[i]
        result.append(dct) 
    return result

def find_a(dif_y, dif_x, mod = MOD): # пошук а
    return int((dif_y * int(pow(int(dif_x), -1, int(MOD)))) % mod) # (y1-y2)*(x1-x2)^-1 % MOD

def solve_mod(perm, mod = MOD): # розв'язок системи
    results = []

    y1, y2 = big_to_val(perm[0][0]), big_to_val(perm[1][0])
    x1, x2 = big_to_val(perm[0][1]), big_to_val(perm[1][1])
   
    dif_y = (y1 - y2) % MOD 
    dif_x = (x1 - x2) % MOD

    if dif_x == 0 or dif_y == 0:
        return []

    gcd = egcd(dif_x, MOD) % MOD

    if  gcd == 1:
        a = (find_a(dif_y, dif_x) + MOD) % MOD
        b = (y1 - x1 * a) % MOD
        results.append((a, b))
    else:
        if dif_y % gcd != 0: return []  
         
        dif_y /= gcd
        dif_x /= gcd
        
        mod = MOD / gcd

        a = (find_a(dif_y, dif_x, mod) + MOD) % MOD
        while a < MOD:
            b = (y1 - x1 * a) % MOD
            results.append((a, b))
            a += gcd
    return results

def decode(big, a, b):
    
    big = big_to_val(big)

    big = (big - b)*pow(int(a), -1, int(MOD))  % MOD # Y - b * a^-1 % MOD

    return val_to_big(big)

#main part

text = ""

variant = input("ENTER a variat >> ")

with open(f"./variants.utf8/0{variant}.txt", 'r', encoding="utf8") as file: 
    lines = file.readlines()
    for line in lines: text += line

text = "".join([i for i in text if i in ABC]) # очистка тексту 
bigrams = crt_bigrams(text)
bigrams2 = Counter(bigrams) # обчислення кількості біграм

popular_bir = get_popular_big(bigrams2, 5) # визначення популярних

perms = get_permutations(popular_bir, PB) # перестановки виду ШФ в ВТ

kek = []

for per in perms: # перетворення в список
    for elem in list(per.items()):
        kek.append(elem)

perms = list(set(kek)) # відкидання дублікатів

comb = combinations(perms, 2) # вз'яття комбінацій для системи рівнянь y1 x1, y2 x2 

keys = [] # (a, b)
i = 0
for c in comb: 
    i +=1
    keys.extend(solve_mod(c)) # обчислення ключів
#print(i)


def analyze(text):
    # неможливі біграми
    miss = ['ьь','аы','аь','чщ','йь','оы','уы','уь']
    ABC1 = 'бвгджзклмнпрстфхцчшщ' # алфавіт
    ABC2 = 'аеиоуыэюя' # алфавіт

    if text == "":# пустий текст
        return False
    for i in range(len(text)-10): # перевірка на 5 приголосних підряд фбо 5 голосних підряд
        if (text[i] in ABC1) and (text[i+1] in ABC1) and (text[i+2] in ABC1) and (text[i+3] in ABC1) and (text[i+4] in ABC1):
            return False
        if (text[i] in ABC2) and (text[i+1] in ABC2) and (text[i+2] in ABC2) and (text[i+3] in ABC2) and (text[i+4] in ABC2):
            return False

    for m in miss:# неможливі біграми
        if m in text:
            return False

    return True


file = open("keys.txt", "w")

for key in list(set(keys)): # перебір можливих ключів
    maybetext = ""
    for big in bigrams[:90]: # взяття перших 30 біграм
        try:
            decode(big, key[0], key[1]) # спроба задекодить
        except:
            check = True
        else:
            maybetext += decode(big, key[0], key[1]) # зберігання тексту

    if analyze(maybetext):
        print(f"({key[0]},{key[1]}) ",maybetext)
        ans = input("Enter y if it`s correct >>")
        if ans == "y":
            break

if ans == "y":
    a = int(key[0])
    b = int(key[1])

    new_text = ""
    for big in bigrams:
        new_text += decode(big, a, b) # ключ 654 / 777
    print(new_text)
