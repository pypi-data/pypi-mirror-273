import re


def clean_html(self, text: str) -> str:
    """
    Метод clean_html убирает все символы HTML из текста

    return re.sub('<[^<]+?>', '', text) - возвращает текст без элементов HTML

    Параметры
    ------
        '<[^<]+?>' - шаблон для определения элементов HTML
        '' - на что заменяются элементы html
    """
    return re.sub('<[^<]+?>', '', text)
