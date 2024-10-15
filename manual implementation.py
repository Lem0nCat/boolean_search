import wikipedia  # Импорт модуля для работы с Википедией
from nltk.stem import WordNetLemmatizer  # Импорт модуля для лемматизации слов
from nltk.corpus import stopwords  # Импорт модуля для работы со стоп-словами
from collections import defaultdict  # Импорт модуля для создания инвертированного индекса
import os


stop_words = set(stopwords.words('english'))  # Инициализация множества стоп-слов
lemmatizer = WordNetLemmatizer()  # Инициализация объекта для лемматизации


# Удаление всех txt файлов, внутри папки dir
def delete_all_files(dir = 'texts'):
    filelist = [ f for f in os.listdir(dir) if f.endswith(".txt") ]
    for f in filelist:
        os.remove(os.path.join(dir, f))

# Функция для вычисления расстояния Левенштейна между двумя строками
def levenshtein_distance(s, t):
    m = len(s)
    n = len(t)
    d = [[0] * (n + 1) for i in range(m + 1)]  # Инициализация матрицы расстояний

    for i in range(1, m + 1):
        d[i][0] = i

    for j in range(1, n + 1):
        d[0][j] = j
    
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i - 1][j] + 1,      # удаление
                          d[i][j - 1] + 1,      # вставка
                          d[i - 1][j - 1] + cost) # замена   

    return d[m][n]  # Возврат значения разницы между строками


# Функция для получения лемматизированного содержания статей по заданной теме
def get_lematized_content(topic, count):
    # Удаление всех txt файлов в папке
    delete_all_files()

    inverted_index = defaultdict(list)  # Инициализация инвертированного индекса
    
    # Получаем список статей из Википедии по заданной теме
    articles = wikipedia.search(topic, results=count)

    # Получаем содержание каждой статьи и лемматизируем его
    for article in articles:
        try:
            # Получение содержания страницы
            content = wikipedia.page(article).content

            # Запись содержаний в разные файлы
            with open(f'texts/{article}.txt', 'w', encoding='utf-8') as file:
                file.write(content)

            # Лемматизация содержания статьи
            lemmatized_content = [lemmatizer.lemmatize(word.lower()) for word in content.split() if word not in stop_words]

            # Построение инвертированного индекса
            for word in lemmatized_content:
                if article not in inverted_index[word]:
                    inverted_index[word].append(article)
        except:
            pass
    return inverted_index


# Функция для поиска наилучшего совпадения и документов с использованием расстояния Левенштейна
def get_best_matches(inverted_index, query_word):
    best_match = ""
    worst_score = 9999999999999999999999999
    best_documents = []

    # Поиск наилучшего совпадения
    for word, documents in inverted_index.items():
        score = levenshtein_distance(query_word, word)
        if score < worst_score:
            worst_score = score
            best_match = word
            best_documents = documents

    return best_match, best_documents

# Пример использования функции
topic = "India" # Тема статей для википедии
inverted_index = get_lematized_content(topic, 10)

# Сравнение слов с помощью дистанции Левенштейна
query_word = "indiian"  # Слово которое нужно найти
best_match, best_documents = get_best_matches(inverted_index, query_word)

print(f"Лучшее совпадение: {best_match} \n Найдено в документах: \n{best_documents}")
