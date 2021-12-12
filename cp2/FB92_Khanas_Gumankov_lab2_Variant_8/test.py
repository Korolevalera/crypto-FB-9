import collections
import sys
import string
import xlwt
from xlwt import Workbook
from math import log2



# function that i used to filter all chars that interfere entropy counting
def prefilter_text(alphabet, filename):
    with open(filename, "r", encoding='utf-8') as f:
        my_text = f.read().lower()
        my_text = my_text.replace("\n", " ").replace("\r", "").replace("\t", " ").replace("ё", "е")
        for char in my_text[:]:
            if char not in alphabet:
                my_text = my_text.replace(char, " ")
        my_text = " ".join(my_text.split())
        return my_text


def count_char_frequency(text_to_read, alphabet):
    char_frequency_counted = {}
    for char in alphabet:
        count_the_char = text_to_read.count(char)
        char_frequency_counted[char] = count_the_char / len(text_to_read)
    return sorted(char_frequency_counted.items(), key=lambda x: x[1], reverse=True)

def encode_text(text_to_encode, cipherkey, alphabet):
    result = ''
    for counter, letter in enumerate(text_to_encode):
        index_of_cipherkey = counter % len(cipherkey)
        result += alphabet[(alphabet.index(letter) + alphabet.index(cipherkey[index_of_cipherkey])) % len(alphabet)]
    return result


def decode_text(text_to_decode, cipherkey, alphabet):
    result = ''
    for counter, letter in enumerate(text_to_decode):
        index_of_cipherkey = counter % len(cipherkey)
        result += alphabet[(alphabet.index(letter) - alphabet.index(cipherkey[index_of_cipherkey])) % len(alphabet)]
    return result


def compliance_index(text_to_calculate, alphabet):
    index = 0
    for letter in alphabet:
        letter_count = text_to_calculate.count(letter)
        index += letter_count * (letter_count - 1)
    return index / (len(text_to_calculate) * (len(text_to_calculate) - 1))


def theoretical_index(text_to_calculate, alphabet):
    char_frec_with_whitespace = count_char_frequency(alphabet, text_to_calculate)
    result = 0
    for i in char_frec_with_whitespace:
        result+=pow(i[1],2)
    return result


def to_the_blocks(text, r):
    blocks = []
    for i in range(r):
        blocks.append(text[i::r])
    return blocks

def find_r(encoded_text, theoretical_index_value, alphabet):

    index_length = {}
    true_index = {}
    one_true_index = {}
    for r in range(2, 31):
        index = 0
        blocks = to_the_blocks(encoded_text, r)
        for block in blocks:
            index += compliance_index(block, alphabet)
        index /= len(blocks)
        index_length[r] = index
        true_index [r] = abs(index - theoretical_index_value)   
    # one_true_index = list(dict(sorted(index_length.items(), key=lambda x: x[1], reverse=False)))[:1]
    # print('Possible key lenght : ')
    # print(one_true_index)
    #print(index_length)
    return dict(sorted(index_length.items(), key=lambda x: x[1], reverse=True))



def find_r_and_write(encoded_text, theoretical_index_value, alphabet,outputfile):

    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    index_length = {}
    true_index = {}
    one_true_index = {}
    for r in range(2, 31):
        index = 0
        blocks = to_the_blocks(encoded_text, r)
        for block in blocks:
            index += compliance_index(block, alphabet)
        index /= len(blocks)
        index_length[r] = index
        sheet1.write(0, r, str(r))
        sheet1.write(1, r, index)
        true_index [r] = abs(index - theoretical_index_value)
        
    # one_true_index = list(dict(sorted(index_length.items(), key=lambda x: x[1], reverse=False)))[:1]
    # print('Possible key lenght : ')
    # print(one_true_index)
    wb.save(outputfile)
    print(index_length)
    return dict(sorted(index_length.items(), key=lambda x: x[1], reverse=True))


def char_frequency(some_text, alphabet):
    freq_dict = {}
    for char in alphabet:
        char_count = some_text.count(char)
        freq_dict[char] = char_count / len(some_text)
    return dict(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))


def find_key(encoded_text, key_length, alphabet):
    blocks = to_the_blocks(encoded_text, key_length)
    top_chars_in_russ = "оаеин"
    maybe_keys = []
    for char in top_chars_in_russ:
        key = ""
        for block in blocks:
            most_used_letter_encoded_text = list(char_frequency(block,alphabet).keys())[0]
            part_of = alphabet[
                (alphabet.index(most_used_letter_encoded_text) - alphabet.index(char)) % len(alphabet)
                ]
            key += part_of
        maybe_keys.append(key)
    return maybe_keys


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        exit("No arguments")
    a = ord('а')
    russ_alphabet_without_whitespace = [chr(i) for i in range(a, a + 32)]
    # print (russ_alphabet)
    my_keys = ['ты', 'нож', 'сила', 'народ', 'абсолютизм', 'авангардист', 'автоматичный', 'аккредитовать', 'автоблокировка', 'аргументировать', 'акклиматизировать', 'вероотступничество' , 'благотворительность', 'золотопромышленность']




    filtered_text_with_whitespaces = prefilter_text(russ_alphabet_without_whitespace, sys.argv[1])
    new_filename = 'filtered_text_with_whitespaces' + str(sys.argv[1])
    with open(new_filename, 'w', encoding='utf-8') as f:
        f.write(filtered_text_with_whitespaces)
        f.close()

    filtered_text_without_whitespaces = filtered_text_with_whitespaces.translate(
        {ord(c): None for c in string.whitespace})
    new_filename = 'filtered_text_without_whitespaces' + str(sys.argv[1])
    with open(new_filename, 'w', encoding='utf-8') as f:
        f.write(filtered_text_without_whitespaces)
        f.close()



    teor_index_for_start_text = theoretical_index(filtered_text_without_whitespaces, russ_alphabet_without_whitespace)
    comp_index_for_start_text = compliance_index(filtered_text_without_whitespaces,russ_alphabet_without_whitespace)
    print("Theoretical index:" + str(teor_index_for_start_text))
    print("Compliance index:" + str(comp_index_for_start_text))


    indexes_in_whole = {}
    counter = 0
    wb2 = Workbook()
    sheet2 = wb2.add_sheet('Sheet 1')
    for key in my_keys:
        
        print(f"Key length: {len(key)}")
        encoded_text_with_key = encode_text(filtered_text_without_whitespaces, key, russ_alphabet_without_whitespace)
        decoded_text_with_key = decode_text(encoded_text_with_key, key, russ_alphabet_without_whitespace)
        compliance_index_for_encoded_text = compliance_index(encoded_text_with_key, russ_alphabet_without_whitespace)
        print(f"Encoded text: {encoded_text_with_key}")
        print(f"Key: {key}")
        print(f"Decoded text: {decoded_text_with_key}")
        print(f"Index: {compliance_index_for_encoded_text}")
        print(f"Possible lengths of a key: {find_r(encoded_text_with_key,teor_index_for_start_text , russ_alphabet_without_whitespace)}")
        print('____________________________________________________________________________________')
        print('____________________________________________________________________________________')
        print('____________________________________________________________________________________')
        indexes_in_whole[key] = compliance_index_for_encoded_text  
        print('Counter : '+ str(counter))
        sheet2.write(1, counter, str(key))
        sheet2.write(2, counter, str(compliance_index_for_encoded_text))
        counter += 1
    
    wb2.save('prestuplenie_index.xls')

    print('____________________________________________________________________________________')
    print('____________________________________________________________________________________')
    print('____________________________________________________________________________________')

    print(russ_alphabet_without_whitespace)
    print(len(russ_alphabet_without_whitespace))



    filtered_text_with_whitespaces2 = prefilter_text(russ_alphabet_without_whitespace, sys.argv[2])
    new_filename = 'filtered_text_with_whitespaces' + str(sys.argv[2])
    with open(new_filename, 'w', encoding='utf-8') as f:
        f.write(filtered_text_with_whitespaces2)
        f.close()

    filtered_text_with_whitespaces2 = filtered_text_with_whitespaces2.translate(
        {ord(c): None for c in string.whitespace})

    teor_index_for_start_text = theoretical_index(filtered_text_with_whitespaces2, russ_alphabet_without_whitespace)
    comp_index_for_start_text = compliance_index(filtered_text_with_whitespaces2,russ_alphabet_without_whitespace)



    print("Theoretical index:" + str(teor_index_for_start_text))
    print("Compliance index:" + str(comp_index_for_start_text))

    keys_length = find_r_and_write(filtered_text_with_whitespaces2, teor_index_for_start_text, russ_alphabet_without_whitespace, 'my_encoded_text.xls') #SAVE THIS#
    print("Possible lengths of a key")
    possible_key_length = list(keys_length.keys())[0]
    print(possible_key_length)

    print(find_key(filtered_text_with_whitespaces2, possible_key_length, russ_alphabet_without_whitespace))
    # for k in range(4,30):
    #     print("Current lengths of a key" + str(k))
    #     print(find_key(filtered_text_with_whitespaces2, k, russ_alphabet_without_whitespace))
    print(decode_text(filtered_text_with_whitespaces2, 'улановсеребряныепули', russ_alphabet_without_whitespace))
    # print(filtered_text_with_whitespaces2)

    

