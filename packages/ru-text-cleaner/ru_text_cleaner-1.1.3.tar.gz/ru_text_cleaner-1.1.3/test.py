from src.ru_text_cleaner import TextCleaner
from src.ru_text_cleaner import clean_punctuation
import re

t = TextCleaner(spaces=False)

test = 'Какая-то форматирования-нибудь строка-либо то-то'

print(clean_punctuation(None, text=test))
print(t.clean_text(test))