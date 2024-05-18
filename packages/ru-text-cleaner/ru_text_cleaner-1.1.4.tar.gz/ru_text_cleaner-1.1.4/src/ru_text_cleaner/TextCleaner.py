from . import *


class TextCleaner:
    def __init__(self, spaces=True, punctuation=True, html=True, emoji=True, lower=True,
                 stop_words=True, morpheme=True):

        """
        Метод __init__ инциализирует экземпляр класса TextCleaner

        self.spaces = spaces - Необходимо ли удалять пробелы
        self.punctuation = punctuation - Необходимо ли удалять пунктуацию
        self.html = html - Необходимо ли удалять теги HTML
        self.emoji = emoji - Необходимо ли удалять Emoji
        self.lower = lower - Необходимо ли переводить текст в нижний регистр
        self.stopwords = stop_words - Необходимо ли удалять стоп слова
        self.morpheme = morpheme - Необходимо ли заменять слова на морфемы

        """

        self.spaces = spaces
        self.punctuation = punctuation
        self.html = html
        self.emoji = emoji
        self.lower = lower
        self.stopwords = stop_words
        self.morpheme = morpheme

        self.to_lower = to_lower_text
        self.clean_emoji = clean_emoji
        self.clean_punctuation = clean_punctuation
        self.clean_html = clean_html
        self.clean_space = clean_spaces
        self.clean_stopwords = clean_stopwords
        self.to_morpheme = text_to_morphems

    def clean_text(self, text: str) -> str:

        """ Метод clean_text форматирует текст в зависимости от поставленных флагов"""

        if self.lower:
            text = self.to_lower(self, text)
        if self.emoji:
            text = self.clean_emoji(self, text)
        if self.html:
            text = self.clean_html(self, text)
        if self.punctuation:
            text = self.clean_punctuation(self, text)
        if self.stopwords:
            text = self.clean_stopwords(self, text)
        if self.morpheme:
            text = self.to_morpheme(self, text)
        if self.spaces:
            text = self.clean_space(self, text)

        return text
