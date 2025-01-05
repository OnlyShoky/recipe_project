# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def duration_format(value):
    if value:
        total_minutes = value.total_seconds() // 60
        hours, minutes = divmod(total_minutes, 60)
        if hours > 0:
            return f"{hours} hr {minutes} min" if minutes > 0 else f"{hours} hr"
        return f"{int(minutes)} min"
    return 'N/A'
