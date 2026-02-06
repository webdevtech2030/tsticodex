import jdatetime
from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name="jalali")
def jalali(value):
    if not value:
        return ""
    dt = timezone.localtime(value) if hasattr(value, "tzinfo") else value
    return jdatetime.datetime.fromgregorian(datetime=dt).strftime("%Y/%m/%d %H:%M")
