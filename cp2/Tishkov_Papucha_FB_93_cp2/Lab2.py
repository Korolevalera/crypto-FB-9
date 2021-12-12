#coding=UTF-8
import random
import pandas as pd
from collections import Counter
from pandas.core.frame import DataFrame

rus_alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я']

rus_alphabet_full = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                     'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                     'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']


def cut_spaces(text):
    new_text_list = list()
    for ch in text:
        if ch != '\n' and ch != ' ':
            new_text_list.append(ch)
    return ''.join(new_text_list)


class TextAnalysisModule:

    def __init__(self, alphabet):
        self.alphabet = alphabet

    def calc_relativity_index(self, text):
        numerator = 0
        for i in Counter(text).values():
            numerator += i * (i - 1)
        n = len(text)
        relativity_index = numerator / ((n - 1) * n)
        return relativity_index

    def find_most_freq_letter(self, text):
        freq_dict = Counter(text)
        return max(freq_dict, key=freq_dict.get)


class VigenereCypherModule:

    def __init__(self, alphabet):
        self.alphabet = alphabet

    def generate_key(self, size):
        key_list = list()
        for i in range(0, size):
            key_list.append(random.choice(self.alphabet))
        return ''.join(key_list)

    def encrypt_letter(self, ch, key_letter):
        enc_ch = self.alphabet[(self.alphabet.index(ch) + self.alphabet.index(key_letter)) % len(self.alphabet)]
        return enc_ch

    def encrypt(self, text, key):
        enc_text_list = list()
        for i, j in enumerate(text):
            enc_text_list.append(self.encrypt_letter(j, key[i % len(key)]))
        return "".join(enc_text_list)

    def decrypt_letter(self, enc_ch, key_letter):
        dec_ch = self.alphabet[(self.alphabet.index(enc_ch) - self.alphabet.index(key_letter)) % len(self.alphabet)]
        return dec_ch

    def decrypt(self, enc_text, key):
        dec_text_list = list()
        for i, j in enumerate(enc_text):
            dec_text_list.append(self.decrypt_letter(j, key[i % len(key)]))
        return "".join(dec_text_list)


class Log:
    def __init__(self, analysis_module, vigenere_module):
        self.analysis_module = analysis_module
        self.vigenere_module = vigenere_module

    def generate_table_of_enc_and_indexes(self, text, key_len_list, log_file='index_table'):
        keys_dict = {}
        enc_texts_dict = {}
        relativity_indexes_dict = {}

        for i in sorted(key_len_list):
            keys_dict.update({i: 0})
            enc_texts_dict.update({i: 0})
            relativity_indexes_dict.update({i: 0})
        for i in key_len_list:
            key = self.vigenere_module.generate_key(i)
            enc_text = self.vigenere_module.encrypt(text, key)
            keys_dict.update({i: key})
            enc_texts_dict.update({i: enc_text[0:39]})
            relativity_indexes_dict.update({i: self.analysis_module.count_considence_index(enc_text)})
        table = pd.DataFrame({'Key': keys_dict.values(),
                              'relativity': relativity_indexes_dict.values(),
                              'Enc. text': enc_texts_dict.values()}, index=key_len_list)
        if log_file is not None:
            table.to_excel(log_file + '.xlsx')

    def guess_key_size_log(self, relativity_indexes_dict, log_file):
        for i in relativity_indexes_dict.keys():
            for j in range(max(relativity_indexes_dict.keys()) - i):
                relativity_indexes_dict[i].append(0)
        log_of_process_df = DataFrame(relativity_indexes_dict)
        log_of_process_df.to_excel(log_file + '.xlsx')


class HackTheKey:

    def __init__(self, vigenere_module, analysis_module, alphabet, max_diff=0.005, relativity_index_of_rus_lang=0.0553):
        self.vigenere_module = vigenere_module
        self.analysis_module = analysis_module
        self.alphabet = alphabet
        self.max_diff = max_diff
        self.relativity_index_of_rus_lang = relativity_index_of_rus_lang
        self.log = Log(analysis_module, vigenere_module)

    def divide_to_blocks(self, text, num):
        text_blocks_list = []
        for i in range(0, num):
            let_num = i
            new_block = []
            while let_num < len(text):
                new_block.append(text[let_num])
                let_num += num
            text_blocks_list.append(''.join(new_block))
        return text_blocks_list

    def guess_key_size(self, enc_text, max_key_size, log_file=None):
        target_key_size = int()
        relativity_indexes_dict = dict()
        for i in range(2, max_key_size + 1):
            numerator = 0
            indexes_list = list()
            text_blocks = self.divide_to_blocks(enc_text, i)
            for block in text_blocks:
                index = self.analysis_module.calc_relativity_index(block)
                numerator += index
                indexes_list.append(round(index, 6))
            relativity_indexes_dict.update({i: indexes_list})
            average = numerator / i
            diff = abs(self.relativity_index_of_rus_lang - average)
            if diff < self.max_diff:
                target_key_size = i
                break
        if log_file is not None:
            self.log.guess_key_size_log(relativity_indexes_dict, log_file)
        return target_key_size

    def guess_key(self, enc_text, key_size):
        text_blocks = self.divide_to_blocks(enc_text, key_size)
        key_letter_list = []
        for block in text_blocks:
            most_freq_letter = self.analysis_module.find_most_freq_letter(block)
            most_freq_letter_id = self.alphabet.index(most_freq_letter)
            shift = (most_freq_letter_id - self.alphabet.index('о')) % len(self.alphabet)
            predictable_letter = self.alphabet[shift]
            key_letter_list.append(predictable_letter)
        return ''.join(key_letter_list)


def main():
    with open('text_lab2.txt', 'r') as text_file:
        enc_text = cut_spaces(text_file.read())
        analysis = TextAnalysisModule(rus_alphabet_full)
        vigenere = VigenereCypherModule(rus_alphabet_full)
        log = Log(analysis, vigenere)
        hack_the_key = HackTheKey(vigenere, analysis, rus_alphabet_full)
        target_key_size = hack_the_key.guess_key_size(enc_text, 32, 'task3')
        print("Key size is: " + str(target_key_size))

        # This is the most close key
        target_key = hack_the_key.guess_key(enc_text, target_key_size)
        print("Key is: " + target_key)

        # Decryption with true guessed key
        guessed_key = 'крадущийсявтени'
        target_text = vigenere.decrypt(enc_text, guessed_key)
        print('\n\n\n--------------------TEXT---------------------------')
        print(target_text)
        output_file = open('decrypted_text.txt', 'w')
        output_file.write(target_text)
        output_file.close()


if __name__ == '__main__':
    main()
