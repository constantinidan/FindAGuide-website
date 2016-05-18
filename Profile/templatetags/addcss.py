from django import template
register = template.Library()

"""
    This file defines the addcss templatetag that allows to set the css style of a given form inside the html template
    instead of doing it inside the django form class which would not be a good separation of model and templates
"""

@register.filter(name='addcss')
def addcss(form, css):
	# css is a string with css fields and their parameters given
	# as "field1:param1,field2:param with spaces,field3: etc..."
	
	css = css.split(',');

	for field in css:
		field = field.split(':')
		form.field.widget.attrs.update({field[0] : field[1]})
	
	return form

