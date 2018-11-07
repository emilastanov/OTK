# Подключаем необходимые библиотеки
import itertools
import numpy as np
import pandas as pd
from math import log2


# Проверка числа, является ли оно степенью двойки
def is_pow_2(number):
    return int(log2(number)) == float(log2(number))

class OTK:
    def __init__(self, word):
        self.word = word
        self.encoded_word = None

    # Функция для представления кодового слова в виде 101?0??
    def getСode(self,word):
        word_iterator = 0
        bit_iterator = 1
        q_code = ''
        while word_iterator < len(word):
            if is_pow_2(bit_iterator):
                q_code += '?'
            else:
                q_code += word[word_iterator]
                word_iterator += 1
            bit_iterator += 1
        return q_code

    # Функция создания матрицы, по которой будет осуществлена подстановка 1 или 0 вместо "?"
    def initMatrix(self,column_indexes, row_indexes):
        matrix = np.zeros([len(row_indexes), len(column_indexes)])
        for c in range(0, len(column_indexes)):
            for r in range(0, len(row_indexes)):
                if column_indexes[c] <= row_indexes[r]:
                    if matrix[r].sum() + column_indexes[c] \
                            <= row_indexes[r]:
                        matrix[r][c] = column_indexes[c]
        return matrix

    # Функция кодирования
    def encodeHamming(self,word):
        q_code = self.getСode(word)
        column_indexes = []
        row_indexes = []
        for i in range(0, len(q_code)):
            if q_code[i] == '?':
                column_indexes.append(i + 1)
            elif q_code[i] == '1':
                row_indexes.append(i + 1)
        column_indexes = np.array(column_indexes)[::-1]
        matrix = self.initMatrix(column_indexes, row_indexes)
        encoded_code = list(q_code)
        for c in range(0, len(column_indexes)):
            matrix[:, c] /= column_indexes[c]
            _sum = matrix[:, c].sum()
            if _sum % 2 == 0:
                encoded_code[column_indexes[c] - 1] = '0'
            else:
                encoded_code[column_indexes[c] - 1] = '1'
        return ''.join(encoded_code)

    # Функция декодирования
    def decodeHamming(self,word):
        column_indexes = []
        row_indexes = []
        for i in range(0, len(word)):
            if is_pow_2(i + 1):
                column_indexes.append(i + 1)
            if word[i] == '1':
                row_indexes.append(i + 1)
        column_indexes = np.array(column_indexes)[::-1]
        matrix = self.initMatrix(column_indexes, row_indexes)
        errors = []
        decoded_code = []
        for c in range(0, len(column_indexes)):
            matrix[:, c] /= column_indexes[c]
            _sum = matrix[:, c].sum()
            if _sum % 2 != 0:
                errors.append(column_indexes[c])
        if sum(errors) == 0:
            for i in range(0, len(word)):
                if not is_pow_2(i + 1):
                    decoded_code.append(word[i])
            return ''.join(decoded_code)
        try:
            pre_decoded_code = list(word)
            decoded_code = []
            error_bit = sum(errors) - 1
            pre_decoded_code[error_bit] = str(1 - int(pre_decoded_code[error_bit]))
            for i in range(0, len(pre_decoded_code)):
                if not is_pow_2(i + 1):
                    decoded_code.append(pre_decoded_code[i])
            return ''.join(decoded_code)
        except Exception as err:
            print(err)
            return None

    # Создание таблицы
    def createTable(self,encoded_word):
        N = len(encoded_word)
        table_data = []
        for i in range(len(encoded_word)):
            errors = list(itertools.combinations(range(N), i))
            C = len(errors)
            decoded_right = 0
            for error in errors:
                error_combinations = list(error)
                err_vector = list(encoded_word)
                if len(error_combinations) == 0 : continue
                for ec in range(0,len(error_combinations)):
                    err_vector[error_combinations[ec]] = str(1 - int(err_vector[error_combinations[ec]]))
                if self.decodeHamming(''.join(err_vector)) == self.word:
                    if i == 2 : print(''.join(err_vector))
                    decoded_right+=1
            table_data.append({"i":i,"C":C,"Nk":decoded_right,"Ck":decoded_right/C},)
        return pd.DataFrame.from_records(table_data,columns=['i','C','Nk','Ck'])

    # Отображение результата
    def getResult(self):
        self.encoded_word = self.encodeHamming(self.word)
        df = self.createTable(self.encoded_word)

        print('Исходный код: {0} | Код Хемминга: {1}\n'.format(self.word,self.encoded_word))
        print(df)

if __name__ == '__main__':
    run = OTK('1010')
    run.getResult()