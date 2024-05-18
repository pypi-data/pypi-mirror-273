import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


def clean_stopwords(self, text: str) -> str:

    """
    Метод clean_stopwords убирает все стоп слова

    stop_words = set(stopwords.words('russian')) - Получает список стоп слов

    words = text.split(' ') - Слова заменяет на пробелы

    for word in words:
        answer += word if word not in stop_words else ''
        answer += ' '
    Убирает стоп слова из текста
    """

    stop_words = set(stopwords.words('russian'))
    words = text.split(' ')
    answer = ''
    for word in words:
        answer += word if word not in stop_words else ''
        answer += ' '

    return answer.strip()
