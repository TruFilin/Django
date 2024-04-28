from django import template

register = template.Library()

# Нежелательные слова, которые будем цензурировать
UNWANTED_WORDS = ['fuck', 'shit', 'bitch']

@register.filter(name='censor')
def censor(value):
    for word in UNWANTED_WORDS:
        value = value.replace(word, '*' * len(word))
    return value

register.filter('censor', censor)
