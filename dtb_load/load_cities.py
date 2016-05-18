import os
import sys
from Profile import models

# This script load cities in the database


liste_villes = [["France", "Paris"], ["UK", "London"], ["Germany", "Berlin"], 
["Czech Republic", "Pragua"], ["Spain", "Madrid"], ["Italy", "Roma"], 
["Russia", "Moscow"], ["Belgium", "Brussels"]]
list_name_town = ["Paris","London","Berlin","Pragua","Madrid","Roma", 
					"Moscow", "Brussels"]


# liste_villes.remove([])
for ville in liste_villes:
 	entree = models.City(city_name=ville[1],country=ville[0])
 	try:
 		entree.save()
 		print (ville[1] + " " + ville[0] + " successfully loaded")
 	except:
 		print(ville[1] + " " + ville[0] + " NOT loaded")
 		pass