from django import template
register = template.Library()


"""
    This file defines the gen_bodyHeaderStyle templatetag which generates the body header css style.
    The goal is to have a city name as a variable parameter 
"""

@register.filter(name='gen_bodyHeaderStyle')
def gen_bodyHeaderStyle(city):

    if city:
        html =  "background: url('/static/img/cities_jpg/"+ city +".jpg') bottom scroll no-repeat;background-size: 100%;"
    else:
        html = ""

    t = template.Template(html)
    return t.render(template.Context({}))


