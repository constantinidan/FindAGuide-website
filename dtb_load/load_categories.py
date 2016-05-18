from Profile import models
from dtb_load.categories import list_category

# This script load categories in the database

for cat in list_category:
	entree = models.Category_Activity(category_name=cat)
	try:
		entree.save()
		print (cat+ " successfully loaded")

	except:
		print (cat+ " NOT loaded")
