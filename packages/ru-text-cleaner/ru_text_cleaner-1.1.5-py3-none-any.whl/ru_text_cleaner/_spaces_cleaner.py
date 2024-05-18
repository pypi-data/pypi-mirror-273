import re

def clean_spaces(self, text: str) -> str:

    """
    Метод clean_spaces убирает лишние пробелы из текста

        re.sub(r' +', ' ', text) - Ищет в переданном тексте лишние пробелы, заменяет их на один пробел
        return text.strip() - Возвращает готовый текст убирая лишние пробелы

        Параметры
        ------
            r' +' - шаблон поиска множества пробелов
            ' ' - на что заменять множества пробелов
            text - сама строка, в которой ищем множества пробелов
    """

    text = re.sub(r'[\uFE00-\uFE0F]', ' ', text)
    text = re.sub('[\t\r\n]', ' ', text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\xa0+', ' ', text)
    return text
