from django import template
from django.utils.html import mark_safe
from django.urls import reverse
import os

register = template.Library()

@register.filter(name="rev")
def do_rev(val):
    return val[::-1]

@register.filter(name="capitalize")
def do_capitalize(val):
    return val.capitalize()

@register.simple_tag
def path(obj, is_file, needs_autoescape=False):
    """
        将 path 展开成对应的链接
        直接传参告知 obj 为目录还是文件，就不去查询判断了
    """
    dir_html = []

    if is_file:
        dir_html.append(obj.name)

    elif not obj.path:
        return ''

    path = obj.path
    while True:
        base = os.path.basename(path)
        dir_html.append('<a href="/{}/{}">{}</a>'.format(obj.owner.username, path, base))
        sub_path = os.path.dirname(path)
        if sub_path == path:
            break
        else:
            path = sub_path
    
    return mark_safe(' / '.join(reversed(dir_html)))
























