from django import template

register = template.Library()


@register.filter
def status(room):
    status = 'info'
    if room.status == 'available':
        status = 'success'
    if room.status == 'not available':
        status = 'danger'
    if room.status == 'reserved':
        status = 'warning'
    return status
