from collections import Counter


class CrackUtils:
    def __init__(self):
        pass

    @staticmethod
    def generate_blocks_of_cipher_text(cipher_text, block_length) -> tuple:
        return block_length, [cipher_text[i::block_length] for i in range(block_length)]

    @staticmethod
    def calculate_blocks_compliance_index(cipher_text_blocks) -> float:
        cipher_text_blocks_indices_list: float = 0
        for cipher_text_block in cipher_text_blocks:
            cipher_text_block_frequency_chars = {
                char: cipher_text_block.count(char) for char in set(cipher_text_block)
            }

            cipher_text_block_compliance_index: float = 0
            for char_frequency in cipher_text_block_frequency_chars:
                cipher_text_block_compliance_index += cipher_text_block_frequency_chars[char_frequency] * (
                        cipher_text_block_frequency_chars[char_frequency] - 1)

            cipher_text_blocks_indices_list += cipher_text_block_compliance_index / (
                    len(cipher_text_block) * (len(cipher_text_block) - 1))

        return cipher_text_blocks_indices_list / len(cipher_text_blocks)

    @staticmethod
    def get_key_length(compliance_indices_dict):
        compliance_index_for_russian_alphabet = 0.057
        return compliance_indices_dict.get(compliance_index_for_russian_alphabet) or compliance_indices_dict[
            min(compliance_indices_dict.keys(), key=lambda key: abs(key - compliance_index_for_russian_alphabet))]

    @staticmethod
    def find_popular_chars_in_cipher_text_by_key_len(cipher_text, key_length):
        popular_chars_list: list = []
        for block in [cipher_text[i::key_length] for i in range(key_length)]:
            popular_chars_list.append(Counter(block).most_common(1)[0][0])
        return popular_chars_list

    @staticmethod
    def get_key(popular_chars_list, alphabet):
        key: str = ''
        for i in range(len(popular_chars_list)):
            key += alphabet[(alphabet.index(popular_chars_list[i]) - 14) % 32]
        return key
