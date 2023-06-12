from django import template

register = template.Library()


@register.filter()
def censor(text):
    bad_words = ['bad', 'author', 'better', 'but', 'отпуск', 'Росси']
    if type(text) == str:
        for i in bad_words:
            text = text.replace(i[1:], '*' * len(i[1:]))
    return text

# Вариант реализации цензор-фильтра из модудя D13.2

# @register.filter
# def hide_forbidden(value):
#     words = value.split()
#     result = []
#     for word in words:
#         if word in forbidden_words:
#             result.append(word[0] + "*"*(len(word)-2) + word[-1])
#         else:
#             result.append(word)
#     return " ".join(result)
