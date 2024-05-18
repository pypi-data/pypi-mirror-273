from src.ru_text_cleaner import TextCleaner

t = TextCleaner()

test = 'Какая-то    форматирования-нибудь \n\n\t строка-либо то-то'

text1 = ['Какая-то    форматирования-нибудь \n\n\t строка-либо то-то', 'Какая-то    форматирования-нибудь \n\n\t строка-либо то-то']
text2 = 'Какая-то    форматирования-нибудь \n\n\t строка-либо то-то'

print(t.clean_texts(text1))
print(t.clean_text(text2))

