from django import template

register = template.Library()

@register.filter(name='multiply')
def multipliy(value, arg):
    if isinstance(value, str) and isinstance(arg, int):
        return str(value) * arg
    else:
        raise ValueError(f'{type(value)} не является строкой или {type(arg)} не является числом')

