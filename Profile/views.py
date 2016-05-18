from django.shortcuts import render
from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse

from guide.mails import *

from .models import City, Guide_Activity, Category_Activity


"""
    This file defines the views of the Profile application.
    The views are called by requests from urls.py,
    They define django template variables that are used in the html between brackets {{}} and {%%}
    They also proceed POST requests submitted inside <form> </form> fields in html templates

    In each view : a dictionnary loc giving the values of local variables is set. Each variable of
    the dictionnary is then usable in the html template inside brackets {{}}
"""


############################ USEFULL FUNCTIONS ##############################
#############################################################################

# This functions is commonly used by ohters. Its checks the common requests of pages
def check_commons(request):
	# set default values
	liForm = LoginForm()
	suForm = SignUpForm()
	has_logout = False
	redirection = None
	new_user=False

	if request.method == "POST":
		# Connexion
		if 'Log in' in request.POST:
			# check login form
			liForm = LoginForm(request.POST)
			if liForm.is_valid():
				username = liForm.cleaned_data["username"]
				password = liForm.cleaned_data["password"]
				user = authenticate(username=username, password=password)
				if user:  # if object is not None
					login(request, user)  # we connect the user
				else: # else an error will be showed
					liForm.userAuthError=True
					user=None
			else:
				liForm.error = True

		elif 'Sign up' in request.POST :
			# check sign up form
			suForm = SignUpForm(request.POST, request.FILES)
			if suForm.is_valid():
				# if form is valid, then user does not exist and can be saved
				username = suForm.cleaned_data["username"]
				password = suForm.cleaned_data["password"]
				email = suForm.cleaned_data["email"]
				suForm.save()
				# login new user
				user = authenticate(username=username, password=password)
				login(request, user)
				# send a mail to new user
				message = "Hey " + username + ", thanks for signing up on FindAGuide !"
				send_email(dest=email,subject='Account confirmation',message=message)
				# tell to redirect on userProfile
				redirection = '/userProfile/new=True'
			else:
				suForm.error = True

		elif 'Log out' in request.POST:
			logout(request)
			has_logout = True

	# return dictionnary of usefull local variables ( instead of just locals() )
	return {"liForm":liForm,
			"suForm":suForm,
			"has_logout":has_logout,
			"redirection":redirection,
			"new_user":new_user,
			}

# this function is used by all views, it returns the new page of the view
def new_page(request,loc, html):
	# check for redirection:
	if loc["redirection"]:
		return HttpResponseRedirect(loc["redirection"])
	# if none, continue on current page
	else:
		return render(request, html, loc)


# checks if a Profile instance has activities or not
def is_guide(guide):
	guid_act = Guide_Activity.objects.filter(guide=guide)
	if guid_act:
		return True
	else:
		return False




############################## VIEWS ################################
#####################################################################


# returns defaults variables for home
def homeDefaults():
	return {"searchCityForm": SearchCityForm(),
			"background_image": "Lisbonne", 
			}
def home(request):
	# check commons first
	loc = check_commons(request)
	# set default values
	loc.update(homeDefaults())

	# check home specific requests
	if request.method == "POST":
		# check search city request
		if 'Search city' in request.POST:
			searchCityForm = SearchCityForm(request.POST)
			if searchCityForm.is_valid():
				city_name = searchCityForm.cleaned_data["cityName"]
				# check if city_name exists
				city = City.objects.filter(city_name=city_name)
				if city:
					loc['redirection'] = '/city=' + city_name
				else:
					searchCityForm.cityError = True
			else:
				searchCityForm.error = True

			# update dict
			loc['searchCityForm'] = searchCityForm

	# return new page
	return new_page(request, loc, 'home.html')

	


# returns defaults variables for userProfile
def userProfileDefaults():
	return {"newActForm": CreateActivityForm(),
			"activities": None,
			"background_image": None,
			"userAvatar": None,
			}
# view for userProfile page
def userProfile(request, new_user=False):

	# check commons first
	loc = check_commons(request)
	# set default values
	loc.update(userProfileDefaults())
	# add city_name parameter
	loc["new_user"] = new_user
	# check if logout
	if loc["has_logout"]:
		loc['redirection'] = '/' # redirect on home page if logged out

	# set user activities and avatar
	if request.user.is_authenticated():
		guide = Profile.objects.get(user=request.user)
		activities = Guide_Activity.objects.filter(guide = guide)
		if not activities:
			activities=None
		loc["activities"] = activities
		loc["userAvatar"] = guide.avatar

	# check userProfile specific requests
	if request.method == "POST":
		# check new activity request
		if 'New activity' in request.POST:
			newActForm = CreateActivityForm(request.POST, request.FILES) 
			if newActForm.is_valid():
				#save it
				newActForm.save(user=request.user)
				loc['redirection'] = '/userProfile'
			else:
				newActForm.error=True

			# update dict
			loc['newActForm'] = newActForm
			
	# return new page
	return new_page(request, loc, 'userProfile.html')




# returns defaults variables for userProfile
def guideProfileDefaults():
	return {"contactForm":ContactForm(),
			"messageSent":False,
			"activities":None,
			"background_image": None,
			"guideAvatar" : None,
			}
# view for giudeProfile page
def guideProfile(request, guide):

	# check commons first
	loc = check_commons(request)
	# set default values
	loc.update(guideProfileDefaults())

	# check existence of guide
	user_g = User.objects.filter(username=guide)
	if user_g:
		user_g = User.objects.get(username=guide)
		guide = Profile.objects.filter(user=user_g) 
		if not guide:
			guide = None
		# check if guide has activities, so if it is actually a guide user
		if not is_guide(guide):
			guide = None
		else:# if user has activities, set guide to the actual value of Profile object
			guide = Profile.objects.get(user=user_g) 
			# set activities
			# set user activities
			activities = Guide_Activity.objects.filter(guide = guide)
			if not activities:
				activities=None
			loc["activities"] = activities
			loc["guideAvatar"] = guide.avatar
	else:
		guide = None

	# add guide parameter
	loc["guide"] = guide
	
	# check guideProfile specific requests
	if request.method == "POST":
		# check Contact guide request
		if "Contact guide" in request.POST:
			contactForm = ContactForm(request.POST)
			if contactForm.is_valid():
				send_contact_email(dest = guide.user.email,
						   subject = contactForm.cleaned_data.get("subject"),
						   message = contactForm.cleaned_data.get("message"),
						   sender = request.user.email,
						   senderUsername = request.user.username)
				contactForm = ContactForm()
				loc["messageSent"]=True
			else:
				contactForm.error=True
			# update dict
			loc['contactForm'] = contactForm

	# return new page
	return new_page(request, loc, 'guideProfile.html')




# returns defaults variables for city
def cityDefaults():
	return {"srchForm": searchActivityForm(),
			"guides":None,
			"activities":None,
			"cityError":False,
			"background_image": None, 
			}
def city(request, city):
	# check commons first
	loc = check_commons(request)
	# set default values
	loc.update(cityDefaults())
	# add city_name parameter
	loc["city_name"] = city
	loc["background_image"] = city

	# check if city request is correct:
	city = City.objects.filter(city_name=city)
	if not city:
		loc["cityError"] = True

	# check city specific requests
	if request.method == "POST":
		# check search guides request
		if 'Search guides or activities' in request.POST:
			srchForm = searchActivityForm(request.POST)

			# check wether if guides or activities asked
			if srchForm.is_valid(): # always valid
				# category name
				category_name = srchForm.cleaned_data.get('category')
				category_name = dict(srchForm.fields['category'].choices)[category_name]
				# guide name : regexp for multiple names ?
				guide_name = srchForm.cleaned_data.get("guide")

				# set guides value
				guides=None
				activities=None

				if guide_name :
					 # use regular expression for better research
					#users = User.objects.get(username__regex='^*'+guide_name+'*')
					users = User.objects.filter(username=guide_name)
					guides=[]

					if users:
						for user in users:
							guide = Profile.objects.filter(user=user)
							if guide and is_guide(guide):
								guides.append( Profile.objects.get(user=user) )
					
					if not guides:
						guides = "empty"

				else:
					city = City.objects.get(city_name=loc["city_name"])
					if category_name == "All categories":
						activities = Guide_Activity.objects.filter(city=city)
						
					else:
						activities = Guide_Activity.objects.filter(city=city, category=category_name)

					if not activities:
						activities = "empty"


				loc["guides"] = guides
				loc["activities"] = activities

		elif 'See profile' in request.method:
			username = request.POST["See profile"]
			loc["redirection"] = '/guide='+username

	# return new page
	return new_page(request, loc, 'city.html')
	
