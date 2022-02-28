from django import template

register = template.Library()

@register.filter(name="censor")
def censor(value, arg):
    result = []
    if arg == "eng":
        swearlist = ["fuck", "shit"] #для данного фильтра логичнее предзадать список значений для разных языков, и обращаться к ним через аргументы
    elif arg == "rus":
        swearlist = ["", ""]  # тут можно сделать более обширный список русских слов, который я пока что заполнять не буду)

    if isinstance(value, str):
        for i in swearlist:
            if i in value:
    #             result.append(value[0] + "*" * (len(value) - 2) + value[-1])
    #         else:
    #             result.append(value)
    # return " ".join(result)
                raise ValueError('Be polite, be-ach!')
    return value

@register.filter(name='update_page')
def update_page(full_path:str, page:int):
    try:
        params_list = full_path.split('?')[1].split('&')
        params = dict([tuple(str(param).split('=')) for param in params_list])
        params.update({'page' : page})
        link = ''
        for key, value in params.items():
            link += (f"{key}={value}&")
        return link[:-1]
    except:
        return f"page={page}"