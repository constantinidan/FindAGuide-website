from django.db import models
from django.contrib.auth.models import User

"""
    This file defines django database models. Please look at the project report on which the UML is presented.
"""

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)  # La liaison OneToOne vers le modele User
    #avatar = models.ImageField(null=True, blank=True, upload_to='../static/static_dirs/img/avatars/', default = '../static/static_dirs/img/default-user.png')
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/')
    description = models.TextField(blank=True)

    def __str__(self):
        return "Profil de {0}".format(self.user.username)

    	
class City(models.Model):
	city_name = models.CharField(max_length=120)
	country = models.CharField(max_length=120)

	class Meta:
		unique_together = ("city_name", "country")

	def __str__(self):
		return ((self.city))


class Category_Activity(models.Model):
	category_name = models.CharField(max_length=120,default='ABC',primary_key=True)
	def __str__(self):
		return ((self.category))
		
# class Guide_city(models.Model):
# 	guide = models.ForeignKey(Profile, on_delete=models.CASCADE)
# 	city = models.ForeignKey(City, on_delete=models.CASCADE)
# 	class Meta:
# 		unique_together = ("city", "guide")


class Guide_Activity(models.Model):
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	guide = models.ForeignKey(Profile, on_delete=models.CASCADE)
	category = models.ForeignKey(Category_Activity, on_delete=models.CASCADE)
	title = models.CharField(max_length=30,default='')
	description = models.CharField(max_length=120,default='')
	image = models.ImageField(null=True, blank=True, upload_to="activities/")




