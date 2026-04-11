from django import template

register = template.Library()


@register.filter
def filename(value):
    """
    从文件路径中提取文件名
    """
    import os
    if value:
        return os.path.basename(str(value))
    return value
