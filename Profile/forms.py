from django import forms
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from .models import Guide_Activity, Profile, City, Category_Activity

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from dtb_load.categories import list_category
from dtb_load.load_cities import list_name_town
import PIL
from PIL import Image

"""
    This file defines django forms. They are then used in views.py and in html templates.

    Clean functions are called in view when is_valid() is called. If an error is raised in a clean function,
    it will appear on the web page to tell the user to change its entry in the form
"""


# transforms a python list of elements into a tuple for form choices with a default value
def list2choices(list_, default=None):
    numbers = [ str(i) for i in range(1,len(list_)+1) ]
    if default:
        return tuple( [('0',default)] + list(zip(numbers, list_))  )
    else:
        return tuple( list(zip(numbers, list_))  )


# to sign up
class SignUpForm(forms.Form):
    email = forms.EmailField(label="Email ",required=True)
    first_name = forms.CharField(label="First name ", max_length= 25, required=True)
    last_name = forms.CharField(label="Last name ", max_length= 25, required=True)
    username = forms.CharField(label="Username ", max_length=30 , required=True)
    password = forms.CharField(label="Password ", widget=forms.PasswordInput, required=True)
    avatar = forms.ImageField(label="Avatar", required=True)
    error = False
    class Meta:
        model = Profile

    # clean functions are called when is_valid() is called
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) == 0 :
            raise forms.ValidationError("Please enter a username")
        
        # now test if username is taken :
        user = User.objects.filter(username=username)
        if user:
            raise forms.ValidationError("Username taken, please change")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if len(email) == 0 :
            raise forms.ValidationError("Please enter a email")
        
        # now test if email is taken :
        em = User.objects.filter(email=email)
        if em:
            raise forms.ValidationError("Email taken, please change")

        return email

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        w, h = get_image_dimensions(avatar)

        #validate dimensions
        max_width = max_height = 1000
        if w > max_width or h > max_height:
            raise forms.ValidationError(
                u'Please use an image that is '
                 '%s x %s pixels or smaller.' % (max_width, max_height))

        #validate content type
        main, sub = avatar.content_type.split('/')
        if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
            raise forms.ValidationError(u'Please use a JPEG, '
                'GIF or PNG image.')

        #validate file size
        if len(avatar) > (100 * 1024):
            raise forms.ValidationError(
                u'Avatar file size may not exceed 20k.')

       
        return avatar

    def save(self, commit=True):
        user = User.objects.create_user(
            first_name = self.cleaned_data.get("first_name"),
            last_name = self.cleaned_data.get("last_name"),
            password = self.cleaned_data.get("password"),
            email = self.cleaned_data.get("email"),
            username = self.cleaned_data.get("username"),
        )

        user.save()
        profile = Profile.objects.create(user = user, avatar=self.cleaned_data.get("avatar"))
        profile.save()
        



# to log in
class LoginForm(forms.Form):
    username = forms.CharField(label="Username ", max_length=30)
    password = forms.CharField(label="Password ", widget=forms.PasswordInput )
    userAuthError = False
    error = False

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) == 0 :
            raise forms.ValidationError("Please enter a username")
        
        # we cannot check here if username exists because it would be a hint for hackers
        # we have to do it elsewhere (in view)
        return username


# to create a new activity
class CreateActivityForm(forms.Form):
    CHOICES_Category = list2choices(list_category, default=None)
    CHOICES_City = list2choices(list_name_town, default=None)
    city = forms.ChoiceField(choices=CHOICES_City, initial='0')
    category = forms.ChoiceField(choices=CHOICES_Category, initial='0')
    title = forms.CharField(label="Title", max_length=30, required=True)
    description = forms.CharField(label="Description", max_length=120, required=True)
    image = forms.ImageField(label="Image", required=True)
    error = False

    class Meta:
        model = Guide_Activity


    def clean_image(self):
        image = self.cleaned_data['image']

        w, h = get_image_dimensions(image)

        #validate dimensions
        max_width = max_height = 300
        if w > max_width or h > max_height:
            raise forms.ValidationError(
                u'Please use an image that is '
                 '%s x %s pixels or smaller.' % (max_width, max_height))

        #validate content type
        main, sub = image.content_type.split('/')
        if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
            raise forms.ValidationError(u'Please use a JPEG, '
                'GIF or PNG image.')

        #validate file size
        if len(image) > (800 * 1024):
            raise forms.ValidationError(
                u'Image file size may not exceed 800k.')
        return image


    def save(self, user, commit=True):
        
        city_name = self.cleaned_data.get("city")
        city_name = dict(self.fields['city'].choices)[city_name]

        # category name
        category_name = self.cleaned_data.get('category')
        category_name = dict(self.fields['category'].choices)[category_name]

        # creact activity and save it
        guide_act = Guide_Activity(
            guide = Profile.objects.get(user=user),
            city = City.objects.get(city_name=city_name),
            category = Category_Activity.objects.get( category_name=category_name ),
            title = self.cleaned_data["title"],
            description = self.cleaned_data["description"],
            image = self.cleaned_data["image"],
        )
        guide_act.save()



class SearchCityForm(forms.Form):
    cityName = forms.CharField(label="Username ", max_length=30)
    error = False
    cityError = False



class searchActivityForm(forms.Form):
    guide = forms.CharField(label="Guide", max_length=30, required=False)
    #category = forms.CharField(label="Category", max_length=30)
    CHOICES = list2choices(list_category , default="All categories")
    category = forms.ChoiceField(choices=CHOICES, initial='0')



class ContactForm(forms.Form):
    subject = forms.CharField(label="Subject",required=True)
    message = forms.CharField(label="Message", max_length= 300, required=True)
    error = False

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message) < 20 :
            raise forms.ValidationError("Your message is too short !")

        # possibility of checking wrong words like insults etc..
        return message

