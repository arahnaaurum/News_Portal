from django import template

register = template.Library()

@register.filter(name="censor")
def censor(value, arg):
    # для данного фильтра логично предзадать список значений для разных языков, и обращаться к ним через аргументы
    swearlist = []
    if arg == "eng":
        swearlist = []
    elif arg == "rus":
        swearlist = []

    if isinstance(value, str):
        for i in swearlist:
            if i in value:
                raise ValueError('Be polite!')
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