from django import template

register = template.Library()

@register.filter
def sortSectionByDayOfWeek(sections):
    for section in sections:
        section.day_of_week_num = section.dayOfWeek()
    return sections
@register.filter
def formatPhoneNumber(phone_number):
    if phone_number:
        p1 = phone_number[0:3]
        p2 = phone_number[3:6]
        p3 = phone_number[6:]
        return f"{p1}-{p2}-{p3}"
    else:
        return '-'