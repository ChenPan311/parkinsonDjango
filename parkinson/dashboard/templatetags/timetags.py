from django import template
from datetime import datetime, timedelta

register = template.Library()


def prettydate(ms):
    if ms < 0:
        date = datetime(1970, 1, 1) + timedelta(seconds=ms/1000)
        date = date.strftime('%d-%m-%Y')
        return date
    else:
        return datetime.fromtimestamp(ms/1000).strftime('%H:%M:%S %d-%m-%Y')


def date_only(ms):
    if ms < 0:
        date = datetime(1970, 1, 1) + timedelta(seconds=ms/1000)
        date = date.strftime('%d-%m-%Y')
        return date
    else:
        return datetime.fromtimestamp(ms/1000).strftime('%d-%m-%Y')


def time_only(ms):
    if ms < 0:
        date = datetime(1970, 1, 1) + timedelta(seconds=ms / 1000)
        date = date.strftime('%d-%m-%Y')
        return date
    else:
        return datetime.fromtimestamp(ms / 1000).strftime('%H:%M:%S')


register.filter(prettydate)
register.filter(date_only)
register.filter(time_only)

