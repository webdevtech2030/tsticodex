from datetime import date, datetime

import jdatetime
from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name="jalali")
def jalali(value):
    if not value:
        return ""
    dt: datetime
    if isinstance(value, str):
        raw = value.replace("T", " ").split("+")[0].strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                parsed = datetime.strptime(raw, fmt)
                dt = parsed
                break
            except ValueError:
                continue
        else:
            return value
    elif isinstance(value, datetime):
        dt = timezone.localtime(value) if timezone.is_aware(value) else value
    elif isinstance(value, date):
        dt = datetime.combine(value, datetime.min.time())
    else:
        return str(value)

    return jdatetime.datetime.fromgregorian(datetime=dt).strftime("%Y/%m/%d %H:%M")
