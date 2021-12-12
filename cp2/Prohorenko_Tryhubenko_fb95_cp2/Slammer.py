import re
from collections import Counter

from CrackUtils import CrackUtils


class Slammer:
    def __init__(self, path_to_file):
        self.keys = ['ой', 'как', 'этот', 'текст', 'зашифровался']
        self.path_to_file = path_to_file
        self.text = self.__getText()
        self.alphabet = self.__initAlphabetDict()

    def __getText(self):
        return re.sub(r"[^а-яА-Я]", "", open(self.path_to_file).read()).lower()

    def __initAlphabetDict(self):
        return [chr(i) for i in range(ord('а'), ord('а') + 32)]

    def __getComplianceIndex(self, text):
        compliance_index: float = 0
        frequency = Counter(text)
        for ch in frequency:
            compliance_index += frequency[ch] * (frequency[ch] - 1)
        compliance_index /= (len(text) * (len(text) - 1))
        return compliance_index

    def encrypt(self):
        print(self.__getComplianceIndex(self.text))
        for key in self.keys:
            cipher_text: str = ''
            for pointer, char in enumerate(self.text):
                plain_char_idx = self.alphabet.index(char)
                key_char_idx = self.alphabet.index(key[pointer % len(key)])
                cipher_text += self.alphabet[(plain_char_idx + key_char_idx) % len(self.alphabet)]
            compliance_index = self.__getComplianceIndex(cipher_text)
            with open(key + '.txt', 'w') as file:
                file.write(cipher_text)
                file.write(f"\n--------------\nCompliance index: {compliance_index}")

    def decrypt(self, path_to_cipher_text, key):
        cipher_text = re.sub(r"[^а-яА-Я]", "", open(path_to_cipher_text).read()).lower()
        plain_text: str = ''
        for pointer, char in enumerate(cipher_text):
            cipher_char_idx = self.alphabet.index(cipher_text[pointer % len(cipher_text)])
            key_char_idx = self.alphabet.index(key[pointer % len(key)])
            plain_text += self.alphabet[(cipher_char_idx - key_char_idx + len(self.alphabet)) % len(self.alphabet)]
        with open(key + '.txt', 'w') as file:
            file.write(plain_text)

    def crack(self, path_to_cipher_text):
        cipher_text = re.sub(r"[^а-яА-Я]", "", open(path_to_cipher_text).read()).lower()

        keys_compliance_indices_dict: dict = {}
        for iterator in range(2, 31):
            key_length, cipher_text_blocks = CrackUtils.generate_blocks_of_cipher_text(cipher_text, iterator)
            cipher_block_compliance_index = CrackUtils.calculate_blocks_compliance_index(cipher_text_blocks)
            keys_compliance_indices_dict[cipher_block_compliance_index] = key_length

        key_length = CrackUtils.get_key_length(keys_compliance_indices_dict)
        popular_chars_list = CrackUtils.find_popular_chars_in_cipher_text_by_key_len(cipher_text, key_length)
        print(keys_compliance_indices_dict)
        key = CrackUtils.get_key(popular_chars_list, self.alphabet)
        return key


s = Slammer("text.txt")
s.encrypt()
key = s.crack("cipher_text_v6.txt")
print("Эй, слушай, я кое-что для тебя нашел, не поможешь?\nНадо всего-то глянуть нет ли "
      f"в этой строчке '{key}' каких-то"
      " ошибочек, \nесли есть - исправь пожалуйста, и верни мне :)")
new_key = input()
s.decrypt("cipher_text_v6.txt", new_key)
print(f"Ты молодец! Если мы всё с тобой сделали правильно - ты найдешь расшифрованный текст в файле {new_key}.txt")