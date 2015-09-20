from django.template import Library

register = Library()


@register.filter
def get_attr(obj, attrname):
    try:
        return getattr(obj, attrname, '')
    except Exception:
        return ''
