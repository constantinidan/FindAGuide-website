#!/usr/bin/env python

# This script automatically reload entirely the database
# At first we though we would use many apps but in fact only Profile was used, so the script loops only on Profile

import subprocess

from guide.settings import INSTALLED_APPS

DEFAULT_INSTALLED_APPS = {
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'sendgrid'
	'south',
	}

INSTALLED_APPS={
	'Profile',
}

class bcolors:
	Red = '\033[91m'
	Green = '\033[92m'
	Blue = '\033[94m'
	Cyan = '\033[96m'
	White = '\033[97m'
	Yellow = '\033[93m'
	Magenta = '\033[95m'
	Grey = '\033[90m'
	Black = '\033[90m'
	Default = '\033[99m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


if __name__ == "__main__":

	## First append commands to command list
	commands = []

	# delete current database
	commands.append('rm -rf db.sqlite3 Profile/migrations')

	# syncdb
	commands.append('python manage.py syncdb')

	# initial
	for app in INSTALLED_APPS:
		if not app in DEFAULT_INSTALLED_APPS:
			commands.append('python manage.py convert_to_south ' + app )
			commands.append('python manage.py schemamigration ' + app + ' --initial')

	# # migrate # apparently unusefull here because of previous schemamigration --initial
	# for app in INSTALLED_APPS:
	# 	if not app in DEFAULT_INSTALLED_APPS:
	# 		commands.append('python manage.py migrate ' + app)

	# data loading
	commands.append('python manage.py shell < auto_load.py')


	## Then execute commands
	for com in commands:
		print(bcolors.BOLD + bcolors.Cyan + "Executing : " + com + bcolors.ENDC)
		err = subprocess.call([com],shell=True)
		if err == 1:
			ans = ''
			while(True):
				ans = input(bcolors.BOLD + bcolors.Blue + "Continue ? " + bcolors.ENDC)
				if ans.lower() in ['yes','']:
					break
				elif ans.lower() == 'no':
					exit()
				else:
					print('Please enter yes (or press Enter), or enter no')


