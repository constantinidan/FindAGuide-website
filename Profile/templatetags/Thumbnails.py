from django import template
from django.conf import settings

"""
    This function generates thumbnails and modals on given number of columns with given generating functions
"""


def generate_thumbnails_and_modals(generate_thumbnail, generate_modal, list_, ncols=4):
    
    html = ""
    counter=0

    # For each element compute its thumnail and add it to html
    # Each ncols activities, make a new row
    for element in list_:
        if counter%ncols == 0:
            html += "\n<div class='row'>"

        html += "\n\n" + generate_thumbnail(element, "modal_"+str(counter) )

        if counter%ncols == ncols-1 or counter == len(list_)-1:
            html += "\n</div>"

        counter+=1


    # then generate modals of each element
    counter=0
    for element in list_:
        html += "\n\n" + generate_modal(element, "modal_"+str(counter) )
        counter+=1

    
    # convert html to template type with void context and return it
    t = template.Template(html)
    return t.render(template.Context({}))

