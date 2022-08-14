from django import template

register = template.Library()


@register.simple_tag(name='read')
def read(file):
    text = file.open()
    return text.read().decode("UTF-8")


@register.filter(name='to_cents')
def to_cents(value):
    return int(value * 100)


@register.filter(name='pluralize')
def pluralize(value):
    retval = ""
    if value > 1:
        retval = "s"
    return retval
