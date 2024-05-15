
'''
	import ramps.browsers.FireFox as FireFox
	FireFox.start ()
'''

'''
	apt install snapd
'''

'''
	apt install wget -y
	wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
	tar -xvzf geckodriver-v0.34.0-linux64.tar.gz

'''

import ramps.climate as climate

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import pathlib
from os.path import dirname, join, normpath
import sys
def driver_path ():
	this_directory = pathlib.Path (__file__).parent.resolve ()
	
	return "/snap/bin/geckodriver"
	
	return str (
		normpath (join (this_directory, "../drivers/gecko/geckodriver"))
	)
	
	

def start ():
	this_climate = climate.find ()

	options = webdriver.FirefoxOptions ()
	if (this_climate.headless == True):
		options.add_argument ("-headless")
		
		
	#
	#	FF profile
	#
	#firefox_profile = FirefoxProfile ()
	#firefox_profile.set_preference ("javascript.enabled", False)
	#options.profile = firefox_profile

	#
	#	https://www.selenium.dev/documentation/webdriver/browsers/firefox/#service
	#
	the_driver_path = driver_path ()
	print ("the_driver_path:", the_driver_path)
	
	
	
	driver = webdriver.Firefox (
		options = options,
		service = webdriver.FirefoxService (
			executable_path = the_driver_path
		)
	)

	return driver;