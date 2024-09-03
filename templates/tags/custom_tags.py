import json

from django import template
register = template.Library()

@register.simple_tag
def makeJsonString(value):
    # Your custom logic here
    return json.dumps(value)