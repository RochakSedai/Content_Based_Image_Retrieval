from django import template
from urllib.parse import urlsplit

register = template.Library()

@register.filter
def gethostname(url):
    hostname = urlsplit(url).netloc
    return hostname