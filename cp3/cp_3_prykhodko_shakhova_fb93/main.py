from itertools import permutations

with open('encrypted.txt', 'r', encoding='utf-8') as file:
    encrypted = file.read()
    encrypted = encrypted.replace('\n', '')


alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р',
            'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']


# розширений алгоритм Евкліда
def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b//a)*x1
    y = x1
    return gcd, x, y


# обернений елемент
def find_reverse_element(a, mod):
    gcd, x, y = gcd_extended(a, mod)
    if gcd == 1:
        return (x % mod + mod) % mod
    else:
        return -1


# розв'язання лінійних рівнянь
def solve_linear_equation(a, b, mod):
    gsd, x, y = gcd_extended(a, mod)
    if gsd == 1:
        x = ((find_reverse_element(a, mod))*b) % mod
        return x
    elif b % gsd != 0:
        return -1
    else:
        a1 = a / gsd
        b1 = b / gsd
        n1 = mod / gsd
        x0 = solve_linear_equation(a1, b1, n1)
        return int(x0)


# біграму перетворюємо в число
def number_for_bigram(bigram, mod):
    return alphabet.index(bigram[0]) * mod + alphabet.index(bigram[1])


# отримаємо біграму з числа
def bigram_from_number(number, mod):
    return alphabet[number//mod]+alphabet[number % mod]


# зашифрувати біграму
def encrypt_bigram(a, b, mod, bigram):
    X = number_for_bigram(bigram, mod)
    Y = (a*X + b) % (mod*mod)
    return bigram_from_number(Y, mod)


# розшифрувати біграму
def decrypt_bigram(a, b, mod, bigram):
    Y = number_for_bigram(bigram, mod)
    X = (find_reverse_element(a, mod*mod)*(Y-b)) % (mod*mod)
    return bigram_from_number(X, mod)


# зашифрувати текст
def encrypt(a, b, mod, text):
    encrypt = []
    text = [text[i:i + 2] for i in range(0, len(text), 2)]
    for i in range(len(text)):
        encrypted = (encrypt_bigram(a, b, mod, text[i]))
        encrypt.append(encrypted)
    return ''.join(encrypt)


# розшифрувати текст і також проаналізувати його на змістовність
def decrypt(a, b, mod, text):
    decrypt = []
    text = [text[i:i + 2] for i in range(0, len(text), 2)]
    for i in range(len(text)):
        decrypted = (decrypt_bigram(a, b, mod, text[i]))
        decrypt.append(decrypted)
    decrypt = ''.join(decrypt)
    if decrypt.count('о')/len(decrypt) < 0.10 or decrypt.count('а')/len(decrypt) < 0.07:
        return -1
    else:
        return decrypt


# отримати ключ за припущенням про перехід двох біграм
def make_key(x1, x2, y1, y2, mod):
    Y = number_for_bigram(y1, mod)-number_for_bigram(y2, mod)
    X = number_for_bigram(x1, mod) - number_for_bigram(x2, mod)
    a = solve_linear_equation(X, Y, mod*mod)
    b = (number_for_bigram(y1, mod)-a*number_for_bigram(x1, mod)) % (mod*mod)
    return [a, b]


# набільш часті біграми відкритого тексту та зашифрованого
top_open = ['ст', 'но', 'ен', 'ни', 'от']
encrypted_top = ['вн', 'тн', 'дк', 'хщ', 'ун']


# створення можливих ключів
def make_possible_keys(top_open, top_encrypted):
    all_top = list(permutations(top_open,2))
    all_enc = list(permutations(top_encrypted,2))

    all_perms = []
    for i in range(len(all_top)):
        all_perms.append(all_top[i]+all_enc[i])

    possible_keys = []
    for i in range(20):
        possible_keys.append(make_key(all_perms[i][0], all_perms[i][1], all_perms[i][2], all_perms[i][3], 31))
    return possible_keys


# отримали список можливих ключів
keys = make_possible_keys(top_open, encrypted_top)


# кожним ключем розшифровуємо текст та фільтруємо
def decrypt_and_analize(encrypted, mod, keys):
    for i in range(len(keys)):
        text = decrypt(keys[i][0], keys[i][1], mod, encrypted)
        if text == -1:
            continue
        else:
            print(keys[i])
            print(text)


decrypt_and_analize(encrypted, 31, keys)

# result (654,777)

