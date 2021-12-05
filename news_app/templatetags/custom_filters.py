from django import template

register = template.Library()

@register.filter(name="censor")
def censor(value, arg):
    if arg == "eng":
        swearlist = ["fuck", "shit"] #для данного фильтра логичнее предзадать список значений для разных языков, и обращаться к ним через аргументы
    elif arg == "rus":
        swearlist = ["", ""]  # тут можно сделать более обширный список русских слов, который я пока что заполнять не буду)

    if isinstance(value, str):
        for i in swearlist:
            if i in value:
                raise ValueError('Be polite, be-ach!')
    return value