from django import template
from django.conf import settings

import Profile.templatetags.Thumbnails as Thumbnails
from Profile.models import Guide_Activity

register = template.Library()

"""
    This file defines the guideThumbnails templatag wich allows to generate
    the html code for showing guides in thumnails and their associated modals 
"""


def generate_thumbnail(guide,modalname):

    html = """<div class='col-sm-3 col-md-3'> 
                <div class='thumbnail'>
                  <a style="cursor:pointer;" class="" onClick="show_modal('"""+ modalname +"""')">
                    <div class='caption'>
                        <h3>""" +guide.user.username+ """</h3>
                    </div>
                    <img src="""+guide.avatar.url+""" alt=''>
                  </a>
                </div>
                <div class='desc hidden'>Post 1 description</div>

              </div>"""

    return html

def generate_modal(guide,modalname):

    html =  """
            <!-- Modal for """ + guide.user.username + """ -->
            <div class='modal fade' id='"""+ modalname +"""' tabindex='-1' role='dialog'>
              <div class='modal-dialog modal-lg' role='document'>

              <!-- Modal content-->
                <div class='modal-content'>
                  <div class='modal-header'>
                    <button type='button' class='close' data-dismiss='modal' aria-label='Close'><span aria-hidden='true'>&times;</span></button>
                  </div>
                  <div class='modal-body'>

                    <div class='row row-centered' >
                      <div class='col-md-8 col-centered' >
                        <h4 class='blacktext'>""" + guide.user.username + """</h4>
                        <p class='blacktext'> Activities of this guide :<br>"""
            
    for activity in Guide_Activity.objects.filter(guide = guide):
      html += "- "+ activity.title + " in " + activity.city.city_name + " <br>"



    html+=        """</p>
                      <button class="btn btn-default" onclick="redirect_page('/guide=""" + guide.user.username + """');">See profile</button>
                      
                      
                    </div>

                  </div>
                  
                </div>
                <div class='modal-footer'>
                  
                </div>
              </div>


            </div>
          </div>"""

    return html


@register.filter(name='guideThumbnails')
def guideThumbnails(guide_list):
    
    return Thumbnails.generate_thumbnails_and_modals(list_ = guide_list, ncols=4, generate_thumbnail=generate_thumbnail, generate_modal=generate_modal)
