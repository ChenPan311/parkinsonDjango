from django import template
import datetime

register = template.Library()


def prettydate(ms):
    date = datetime.datetime.fromtimestamp(ms / 1000.0)
    date = date.strftime('%H:%M:%S %d-%m-%Y')
    return date


def date_only(ms):
    date = datetime.datetime.fromtimestamp(ms / 1000.0)
    date = date.strftime('%d-%m-%Y')
    return date


def time_only(ms):
    date = datetime.datetime.fromtimestamp(ms / 1000.0)
    date = date.strftime('%H:%M:%S')
    return date


register.filter(prettydate)
register.filter(date_only)
register.filter(time_only)

