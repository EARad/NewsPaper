from django import template
from random import sample

register = template.Library()


@register.filter(name='censor')
def censor(value):
    list_curse = open("C:\\Users\\Lezik\\pythonProject\\NewsPaper\\NewsPaper\\news\\templatetags\\curse.txt", 'r')
    curse = list_curse.read().split(', ')
    fil = ['@', '#', '$', '%', '^', '&', '*']
    res = []
    new_res = []

    for word in value.split():
        if word.lower() in curse:
            res.append(''.join(sample(fil, len(word))))
        else:
            res.append(word)

    for word in res:
        if '.' or '!' or ',' or '?' in word:
            m = word.find('.' or '!' or ',' or '?')
            new_word = word[:m]
            if new_word.lower() in curse:
                new_res.append(''.join(sample(fil, len(new_word)))+word[m])
            else:
                new_res.append(word)
        else:
            new_res.append(word)

    list_curse.close()
    return (' '.join(new_res))

print(censor('Ебать сука пизда гуси лебеди блядь паук'))