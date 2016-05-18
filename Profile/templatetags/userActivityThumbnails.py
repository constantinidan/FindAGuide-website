from django import template
from django.conf import settings

import Profile.templatetags.Thumbnails as Thumbnails

register = template.Library()


"""
    This file defines the userActivityThumbnails templatag wich allows to generate
    the html code for showing activities (in user Profile) as thumnails, with their associated modals 
"""


def generate_thumbnail(activity,modalname):

    html = """<div class='col-sm-3 col-md-3'> 
                <div class='thumbnail'>
                  <a style="cursor:pointer;" class="" onClick="show_modal('"""+ modalname +"""')">
                    <div class='caption'>
		    			<h3>""" + activity.title + """</h3>
		             </div>
		             <img src="""+activity.image.url+""" alt=''>

                  </a>
                </div>
                <div class='desc hidden'>Post 1 description</div>

              </div>"""

    return html

def generate_modal(activity,modalname):


	html =	"""
			<!-- Modal for """ + activity.title + """ -->
			<div class='modal fade' id='"""+modalname+"""' tabindex='-1' role='dialog'>
			  <div class='modal-dialog modal-lg' role='document'>

			  <!-- Modal content-->
			    <div class='modal-content'>
			      <div class='modal-header'>
			        <button type='button' class='close' data-dismiss='modal' aria-label='Close'><span aria-hidden='true'>&times;</span></button>
			      </div>
			      <div class='modal-body'>

			        <div class='row row-centered' >
			          <div class='col-md-8 col-centered' >
			          	<h4 class='blacktext'>""" + activity.title + """</h4>
			          	<img src="""+activity.image.url+""" alt=''>
			          	<p class='blacktext'>""" + activity.description + """</p>
			           
			          </div>

			        </div>
			        
			      </div>
			      <div class='modal-footer'>
			        
			      </div>
			    </div>


			  </div>
			</div>"""

	return html


@register.filter(name='userActivityThumbnails')
def userActivityThumbnails(activity_list):
    
    return Thumbnails.generate_thumbnails_and_modals(list_ = activity_list, ncols=4, generate_thumbnail=generate_thumbnail, generate_modal=generate_modal)
