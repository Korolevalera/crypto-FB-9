from collections import Counter

#розширений алгоритм евкліда
alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя" # "ё" "ъ" в нашем тексте нет
alen = len(alphabet)
f=open('07.txt', 'r', encoding='utf-8')
encoded_text = f.read()


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

#пошук оберненого
def modinv(a, mod):
    nsd, x, y = egcd(a, mod)
    if nsd != 1:
        return False
    else:
        x = (x % mod + mod) % mod
        return x


def modulation(a, b, mod):  # ax=b modn
    x = [] #Масив з розв
    a = a % mod
    b = b % mod
    nsd = egcd(a, mod)[0]

    if nsd == 1:        # Маємо 1 розв якщо а і мод взаємнопрості :
        x.append((modinv(a, mod)*b)%mod)    #x=b*a^-1 mod n
    elif b % nsd == 0:
            a_rek = a // nsd
            b_rek = b // nsd
            mod_rek = mod // nsd
            x.append((modulation(a_rek, b_rek, mod_rek)[0]))
            for i in range(1, nsd):
                x.append(x[-1] + mod_rek)

    return x




def bigr_to_num(bigr,mod):
    num=alphabet.index(bigr[0])*mod+alphabet.index(bigr[1])
    return num

def num_to_bigr(num, mod):
    bigr=alphabet[num//mod]+alphabet[num % mod]
    return bigr

#перевірка частоти біграм
def freq(txt):
    bigram_arr = []
    for i in range(0, len(txt)-1, 2):
        bigram=txt[i]+txt[i+1]
        bigram_arr.append(bigram)
    c = Counter(bigram_arr)
    return c

#перебір усіх можливих комбінацій найчастіших біграм ШТ і ВТ
def all_keys(top_en, top_plain):
    for i in range(0, len(top_plain)):
        x1= str(top_plain[i])
        x2 = str(top_plain[(i+1)%5])
        for j in range(0, len(top_plain)):
                y1=str(top_en[j])
                y2=str(top_en[(j+1)%5])
             #   print('x1 = ' + x1 + ', x2 = ' + x2 + ',y1 = ' + y1 + ' y2 =' + y2)

                key(x1, x2, y1, y2)


#розшифровка ШТ
def decode (encoded, a, b):
    decoded_txt = []
    for i in range(0, len(encoded)-1, 2):
        mod = alen*alen
        y = encoded[i] + encoded[i + 1]
        y_num = bigr_to_num(y, alen)
        inv_a = modinv(a, mod)
        decoded_bigr = (inv_a*(y_num - b))%mod

        decoded_txt.append(num_to_bigr(decoded_bigr, alen))
    decoded = ''.join(decoded_txt)
    return decoded



#знаходження ключів для даних 4 біграм
def key(x1, x2, y1, y2):
    b = 0
    mod = alen*alen
    arr_key = []
    x = bigr_to_num(x1, alen)-bigr_to_num(x2, alen)
    y = bigr_to_num(y1, alen)-bigr_to_num(y2, alen)
    a = modulation(x, y, mod)

    for i in range(0, len(a)):
            b = (bigr_to_num(y1, alen) - a[i] * bigr_to_num(x1, alen)) % mod

            check1 = key_check_most(a[i], b)
            check2 = key_check_less(a[i], b)

            if check1 == check2 == 1:
                print('x1 = ' + x1 + ', x2 = ' + x2 + ',y1 = ' + y1 + ' y2 =' + y2)
                print('a = ' + str(a[i]) + ', b = ' + str(b))
                print(decode(encoded_text, a[i], b))

def key_check_most(a, b): #перевірка найчастіших літер (о, а, е)
    check = 0
    txt = decode(encoded_text, a, b)
    most_lett = Counter(txt).most_common(3)
    for i in most_lett:
        x, y = i
        if x in top_lett_alphabet:
            check += 1
    if check == 3:
        return 1
    else:
        return 0

def key_check_less(a, b): # перевірка найрідкісніших літер (щ, ф)
        check = 0
        txt = decode(encoded_text, a, b)
        less_lett = list(reversed(Counter(txt)))
        if len(less_lett) == 1:
            return 0
        for i in range(0,2):
            if less_lett[i] in less_lett_alphabet:
                check +=1
        if check == 2:
            return 1
        else:
            return 0


#біграми та літери з найвищою частотою
top_bigr_en=['цл', 'ял', 'ае', 'ле', 'чо']
top_bigr_plain = ['ст', 'но', 'то', 'на', 'ен']
top_lett_alphabet = ['о', 'а', 'е']
less_lett_alphabet = ['ф', 'щ']

#encoded_text.replace(' ', '')

all_keys(top_bigr_en, top_bigr_plain)

f.close()

#print(keys)
#freq(encoded_text)
