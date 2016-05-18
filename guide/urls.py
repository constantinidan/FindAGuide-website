from django.conf.urls import patterns, include, url
from Profile import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

"""
	This file defines the links between urls requests and views' calls
	Some requests use a regular expression to pass a parameter value such as the city name for instance 
"""

admin.autodiscover()
urlpatterns = patterns('',

    url(r'^$', views.home, name='home'),
    url(r'^userProfile/new=(?P<new_user>.*)$', views.userProfile, name='userProfile'),
    url(r'^userProfile/$', views.userProfile, name='userProfile'),
    url(r'^guide=(?P<guide>.*)$', views.guideProfile, name='guideProfile'), # regexp for guide parameter
    url(r'^city=(?P<city>.*)$', views.city, name='city'), # regexp for city parameter
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # add media files url


# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)