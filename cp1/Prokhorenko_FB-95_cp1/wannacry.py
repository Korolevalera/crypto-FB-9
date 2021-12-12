import csv
import math
import re


class WannaCry:
    def __init__(self, pathToFile):
        self.pathToFile = pathToFile
        self.text_with_spaces = re.sub(r"[^а-яА-Я ]", "", self.__getText(pathToFile)).lower()
        self.text_without_spaces = re.sub(r"[^а-яА-Я]", "", self.__getText(pathToFile)).lower()

    def __getText(self, pathToFile):
        return open(pathToFile).read()

    def __getLettersProbability(self):
        frequency_letters_with_spaces = {
            char: self.text_with_spaces.count(char) for char in set(self.text_with_spaces)
        }
        frequency_letters_without_spaces = {
            char: self.text_without_spaces.count(char) for char in set(self.text_without_spaces)
        }
        probability_letter_with_spaces = {
            key: frequency_letters_with_spaces[key] / len(self.text_with_spaces) for key in
            frequency_letters_with_spaces.keys()
        }
        probability_letter_without_spaces = {
            key: frequency_letters_without_spaces[key] / len(self.text_without_spaces) for key in
            frequency_letters_without_spaces.keys()
        }

        return probability_letter_with_spaces, probability_letter_without_spaces

    def __getBigramProbability(self):
        from collections import Counter
        frequency_bigrams_with_spaces = Counter(
            self.text_with_spaces[idx:idx + 2] for idx in range(len(self.text_with_spaces) - 1)
        )
        frequency_bigrams_without_spaces = Counter(
            self.text_without_spaces[idx:idx + 2] for idx in range(len(self.text_without_spaces) - 1)
        )
        probability_bigrams_with_spaces = {
            key: frequency_bigrams_with_spaces[key] / len(self.text_with_spaces) for key in
            frequency_bigrams_with_spaces.keys()
        }
        probability_bigrams_without_spaces = {
            key: frequency_bigrams_without_spaces[key] / len(self.text_without_spaces) for key in
            frequency_bigrams_without_spaces.keys()
        }

        return probability_bigrams_with_spaces, probability_bigrams_without_spaces

    def __getLettersEntropy(self):
        probability_letter_with_spaces, probability_letter_without_spaces = self.__getLettersProbability()
        entropy_letters_with_spaces = 0
        for p in probability_letter_with_spaces.values():
            entropy_letters_with_spaces += -(p * math.log2(p))
        entropy_letters_without_spaces = 0
        for p in probability_letter_without_spaces.values():
            entropy_letters_without_spaces += -(p * math.log2(p))

        return entropy_letters_with_spaces, entropy_letters_without_spaces

    def __getBigramsEntropy(self):
        probability_bigrams_with_spaces, probability_bigrams_without_spaces = self.__getBigramProbability()
        entropy_bigrams_with_spaces = 0
        for p in probability_bigrams_with_spaces.values():
            entropy_bigrams_with_spaces += -(p * math.log2(p))
        entropy_bigrams_without_spaces = 0
        for p in probability_bigrams_without_spaces.values():
            entropy_bigrams_without_spaces += -(p * math.log2(p))

        return entropy_bigrams_with_spaces / 2, entropy_bigrams_without_spaces / 2

    def __getLettersSurplus(self):
        entropy_letters_with_spaces, entropy_letters_without_spaces = self.__getLettersEntropy()
        return (1 - entropy_letters_with_spaces / math.log2(33)), (1 - entropy_letters_without_spaces / math.log2(32))

    def __getBigramsSurplus(self):
        entropy_bigrams_with_spaces, entropy_bigrams_without_spaces = self.__getBigramsEntropy()
        return (1 - entropy_bigrams_with_spaces / math.log2(33)), (1 - entropy_bigrams_without_spaces / math.log2(32))

    def log(self):
        file = open("log.txt", "w", encoding="UTF-8")
        csv.writer(file).writerow(
            [f"\n\n********************* ANALYSING FILE {self.pathToFile} *********************\n\n"])
        for num, type in enumerate(self.__getLettersProbability()):
            csv.writer(file).writerow([f"Output probability letters [{num}]"])
            for key in type:
                csv.writer(file).writerow([key, type[key]])
        for num, type in enumerate(self.__getBigramProbability()):
            csv.writer(file).writerow([f"Output probability bigrams [{num}]"])
            for key in type:
                csv.writer(file).writerow([key, type[key]])
        for num, e in enumerate(self.__getLettersEntropy()):
            csv.writer(file).writerow([f"Output entropy letters [{num}] - {e}"])
        for num, e in enumerate(self.__getBigramsEntropy()):
            csv.writer(file).writerow([f"Output entropy bigrams [{num}] - {e}"])
        for num, e in enumerate(self.__getLettersSurplus()):
            csv.writer(file).writerow([f"Output surplus letters [{num}] - {e}"])
        for num, e in enumerate(self.__getBigramsSurplus()):
            csv.writer(file).writerow([f"Output surplus bigrams [{num}] - {e}"])


wc = WannaCry('text.txt')
wc.log()
