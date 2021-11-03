# -------------------------------------------------
# Лабараторная работа 3 задание 1
#
# Программа генерирует текст на цепях Маркова на 100 слов + псевднослучайное количество вставок смайлика
# затем с помощью регулярных выражений находит количество подстрок в сгенерированном тексте
# и выводит в консоль в оформленном виде
#
# Генератор текста на цепях Маркова
# Код генератора взят с сайта https://thecode.media/markov-text/
# -------------------------------------------------
import re
import numpy as np
import random

# отправляем в переменную всё содержимое текстового файла
text = open('elon.txt', encoding='utf16').read()

# разбиваем текст на отдельные слова (знаки препинания останутся рядом со своими словами)
corpus = text.split()  # массив на 6546 слов


# делаем новую функцию-генератор, которая определит пары слов
def make_pairs(corpus):
    # перебираем все слова в корпусе, кроме последнего
    for i in range(len(corpus) - 1):
        # генерируем новую пару и возвращаем её как результат работы функции
        yield (corpus[i], corpus[i + 1])


# вызываем генератор и получаем все пары слов
pairs = make_pairs(corpus)  # ('первое слово', 'второе слово')

word_dict = {}

# перебираем все слова попарно из нашего списка пар
for word_1, word_2 in pairs:
    # если первое слово уже есть в словаре
    if word_1 in word_dict.keys():
        # то добавляем второе слово как возможное продолжение первого
        word_dict[word_1].append(word_2)
    # если же первого слова у нас в словаре не было
    else:
        # создаём новую запись в словаре и указываем второе слово как продолжение первого
        word_dict[word_1] = [word_2]

# случайно выбираем первое слово для старта
first_word = np.random.choice(corpus)

# если в нашем первом слове нет больших букв
while first_word.islower():
    # то выбираем новое слово случайным образом
    # и так до тех пор, пока не найдём слово с большой буквой
    first_word = np.random.choice(corpus)

# делаем наше первое слово первым звеном
chain = [first_word]

# сколько слов будет в готовом тексте
n_words = 100

string = 'X-('
pattern = r'X-\('
text = r''


def generation_text(n_words, word_dict):
    # делаем цикл с нашим количеством слов
    for i in range(n_words):
        # на каждом шаге добавляем следующее слово из словаря, выбирая его случайным образом из доступных вариантов
        chain.append(np.random.choice(word_dict[chain[-1]]))
        # создаем буфер для следующего ключа, новый ключ не будет существовать, если выполниться условие без буфера
        # так как новым ключом станет X-(, которго нет в словаре word_dict
        buffer = np.random.choice(word_dict[chain[-1]])
        # если условие выполниться
        if random.randint(0, 9) == 0:
            # то добавится смайлик
            chain.append(string)
            # возвращения ключа до выполнения условия
            chain.append(buffer)

    # array --> string
    finallytext = ' '.join(chain)
    return finallytext


def output(finallytext, count):
    # text for find the substring (text test)
    print('Сгенерированный текст номер: ' + str(count))
    print(finallytext, '\n')

    # number of substring matches (Regular expressions)
    print('Количество вхождений подстроки, найденное через регулярные выражения:')
    print(len(re.findall(pattern, finallytext)), '\n')

    # number of substring matches
    print('Количество вхождений подстроки, найденное через метод count:')
    print(finallytext.count(string), '\n')
    print('-----------------------------')
    print('\n')


i = 0
while i < 5:
    output(generation_text(n_words, word_dict), i + 1)
    i += 1
