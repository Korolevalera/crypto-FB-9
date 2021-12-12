import re
from collections import Counter

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
keys = ['ну', 'так', 'даже', 'очень', 'прикольнаялаба']
plaintext = re.sub(r'[^а-яА-Я]', '', open('plaintext.txt').read()).lower()
ciphertext = re.sub(r'[^а-яА-Я]', '', open('ciphertext_v4.txt').read()).lower()


def encrypt(_plaintext, _key):
    _ciphertext = ''
    for num, letter in enumerate(_plaintext):
        _ciphertext += alphabet[(alphabet.index(letter) + alphabet.index(_key[num % len(_key)])) % len(alphabet)]
    return _ciphertext


def conformity_index(text_block):
    quantity = Counter(text_block)
    conformity = 0
    for el in quantity:
        conformity += quantity[el] * (quantity[el] - 1)
    conformity /= len(text_block) * (len(text_block) - 1)
    return conformity


def output(_text):
    for num, _key in enumerate(keys):
        encrypted_text = encrypt(plaintext, _key)
        open(f'key{num}.txt', 'w').write(f'Conformity index: {conformity_index(encrypted_text)}\n\n{encrypted_text}')


def cipher_break(_text):
    russian_conformity_index = 0.0553
    keys_indices = {}
    for key_length in range(2, 33):
        average_index = 0.0
        text_blocks = [_text[i::key_length] for i in range(key_length)]
        for text_block in text_blocks:
            average_index += conformity_index(text_block)
        average_index /= len(text_blocks)
        keys_indices[average_index] = key_length
    true_key_length = keys_indices.get(russian_conformity_index) or keys_indices[
        min(keys_indices.keys(), key=lambda key: abs(key - russian_conformity_index))]
    most_common_chars = []
    for text_block in [_text[i::true_key_length] for i in range(true_key_length)]:
        most_common_chars.append(Counter(text_block).most_common(1)[0][0])
    _key = ''
    for e in range(len(most_common_chars)):
        _key += alphabet[(alphabet.index(most_common_chars[e]) - alphabet.index('о')) % len(alphabet)]
    return _key


def decrypt(_text, _key):
    plain_text: str = ''
    for pointer, char in enumerate(_text):
        plain_text += alphabet[(alphabet.index(_text[pointer % len(_text)]) - alphabet.index(
            _key[pointer % len(_key)]) + len(alphabet)) % len(alphabet)]
    open('decrypted.txt', 'w').write(plain_text)


output(plaintext)

key = cipher_break(ciphertext)
print(f'The possible key is {key}')

key = 'громыковедьма'
print(f'The true key is {key}')
decrypt(ciphertext, key)
