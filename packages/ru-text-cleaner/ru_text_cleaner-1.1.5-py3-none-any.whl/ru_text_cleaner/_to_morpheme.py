import pymorphy2


def text_to_morphems(self, text: str) -> str:

    """
    Метод text_to_morphems заменяет слова на морфемы

    morph = pymorphy2.MorphAnalyzer(lang='ru') - получает список морфем

    for i in text.split(' '):
        mor += morph.parse(i)[0].normal_form
        mor += ' '
    Цикл в катором слова заменяются на морфемы и разделяются пробелом
    """

    morph = pymorphy2.MorphAnalyzer(lang='ru')
    mor = ''
    for i in text.split(' '):
        mor += morph.parse(i)[0].normal_form
        mor += ' '
    return mor
