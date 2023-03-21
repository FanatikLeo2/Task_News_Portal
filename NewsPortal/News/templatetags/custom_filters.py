from django import template

register = template.Library()


@register.filter()
def censor(text):
    bad_words = ['bad', 'author', 'better', 'but', 'отпуск', 'Росси']
    if type(text) == str:
        for i in bad_words:
            text = text.replace(i[1:], '*' * len(i[1:]))
    return text
