from django.template import Library

register = Library()


@register.filter
def get_attr(obj, attrname):
    return getattr(obj, attrname, '')
