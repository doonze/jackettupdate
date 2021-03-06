#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# This file is used to configure and create the config file. It's called from the main app
#JackettUpdate configupdate

import sys
import os
import configparser
from configparser import ConfigParser
from builtins import input

# Now we'll start gathering user input
# First user will choose their distro

print("[1] Linux X64")
print("[2] Linux ARM32")
print("[3] Linux ARM64")
print("[C] Cancel config update")

while True:
	distrochoice = input("Choose your distro by number or C to cancel update [?]: ")
	if str(distrochoice) == "1":
		chosendistro = "Linux X64"
		break
	elif str(distrochoice) == "2":
		chosendistro = "Linux ARM32"
		break
	elif str(distrochoice) == "3":
		chosendistro = "Linux ARM64"
		break
	elif str(distrochoice) == "c" or str(distrochoice) == "C":
		print("")
		print("Exiting config update and installer....")
		print("")
		quit()
	else:
		print("")
		print("Invalid Choice! Valid choices are 1-3 or C to cancel. Please Try again.")
		print("")

print("")
print(chosendistro + " Chosen")
print("")

while True:
  installpath = input("Root filepath to install Jackett? (Suggest /opt/. The Jackett tarball automatically creates a Jackett directory) [/opt/]: ")
  if str(installpath) == "":
    print("")
    print("You must enter a valid filepath!")
  else:
    break
  
print("")
print(installpath + " set as Jackett install root directory")
print("")

while True:
  servicename = input("Name of systemd Jackett service? This is the name it runs on through systemd [ex. jackett]: ")
  if str(servicename) == "":
    print("")
    print("You must enter a service name!")
  else:
    break
  
print("")
print(servicename + " set as Jackett systemd service")
print("")

# Now user chooses beta or Stable releases. Currently Jackett doesn't seem to use prelease (beta) versions. So commenting this out for now.

#while True:
#	choosebeta = input("Do you want to install the beta version? [y/N] ")
#	if choosebeta == "y" or choosebeta == "Y":
#		betachoice = "Beta"
#		break
#	elif choosebeta == "n" or choosebeta == "N" or choosebeta == "":
betachoice = "Stable"
#		break
#	else:
#		print("")
#		print("Invalid choice. Please choose y or n")
#		print("")

#print("")
print(betachoice + " version of Jackett has been chosen for install. This was autoselected as currently Jackett doesn't use prerelease (beta) releases")
print("")

# User chooses if they wish to stop the server before installing updates. Not normally needed. But not a bad idea.

while True:
	servstop = input("Do we need to manually stop the server to install? Use only if you have Jackett running as a service [Y/n]: ")
	if servstop == "y" or servstop == "Y" or servstop == "":
		servstopchoice = "Server will be stopped by the script on install."
		stopserver = True
		break
	elif servstop == "n" or servstop == "N":
		servstopchoice = "Server will NOT be stopped by the script on install."
		stopserver = False
		break
	else:
		print("")
		print("Invalid choice. Please choose y or n")
		print("")

print("")
print(servstopchoice)
print("")

# User chooses if they wish to start the server again after updates. This is needed to pickup update for running version.
while True:
	servstart = input("Do we need to manually start the server after install? Use only if you have Jackett running as a service [Y/n]: ")
	if servstart == "y" or servstart == "Y" or servstart == "":
		servstartchoice = "Server will be started by the script after install."
		startserver = True
		break
	elif servstart == "n" or servstart == "N":
		servstartchoice = "Server will NOT be started by the script after install."
		startserver = False
		break
	else:
		print("")
		print("Invalid choice. Please choose y or n")
		print("")

print("")
print(servstartchoice)
print("")

# User chooses if they wish to autoupdate the Update app (this program)
while True:
	scriptupdate = input("Keep JackettUpdate (this script) up to date with latest version? [Y/n]: ")
	if scriptupdate == "y" or scriptupdate == "Y" or scriptupdate == "":
		scriptupdatechoice = "Script (JackettUpdate) will be automatically updated!"
		autoupdate = True
		break
	elif scriptupdate == "n" or scriptupdate == "N":
		scriptupdatechoice = "Script (JackettUpdate) will NOT be automatically updated!"
		autoupdate = False
		break
	else:
		print("")
		print("Invalid choice. Please choose y or n")
		print("")

print("")
print(scriptupdatechoice)
print("")

print("Choices to write to config file...")
print("Linux distro version to update: " + chosendistro)
print("The chosen version for install is: " + betachoice)
print("The chosen systemd service name is: " + servicename)
print("The chosen install filepath is " + installpath)
print(servstopchoice)
print(servstartchoice)
print(scriptupdatechoice)
print("")

while True:
	confirm = input("Please review above choices and type CONFIRM to continue or c to cancel update and install! [CONFIRM/c] ")
	if confirm == "c" or confirm == "C":
		print("")
		print("Exiting config update and installer. No changes were made and nothing will be installed!")
		print("")
		quit()
	elif confirm == "CONFIRM":
		break
	else:
		print("")
		print("Invalid choice. Please type CONFIRM to continue or c to cancel!!")
		print("")


# Setup the config interface
config = configparser.ConfigParser()

# Test if the config file exist
try:
	if not os.path.isfile("config.ini"):
		cfgexist = False
	else:
		cfgexist = True
except Exception as e:
	print("JackettUpdate: Couldn't access the config.ini file. Permission issues? We can't continue")
	print("JackettUpdate: Here's the error we got -- " + str(e))
	sys.exit(1)
	
	
# If config doesn't exist (cfgexist False) it will create it with the correct values fill in and 
# if it does exist (cfgexist True) it will simply update the existing config
try:
	if cfgexist == False:
		config['DISTRO'] = {'installdistro' : chosendistro, 'releaseversion' : betachoice}
		config['SERVER'] = {'installpath' : installpath, 'servicename' : servicename, 'stopserver' : stopserver, 'startserver' : startserver, 'jackettversion' : "First Run"}
		config['JackettUpdate'] = {'autoupdate' : autoupdate, 'version' : "First Run"}
	elif cfgexist == True:
		config.read('config.ini')
		config['DISTRO']['installdistro'] = chosendistro
		config['DISTRO']['releaseversion'] = betachoice
		config['SERVER']["installpath"] = installpath
		config['SERVER']["servicename"] = servicename
		config['SERVER']['stopserver'] = str(stopserver)
		config['SERVER']['startserver'] = str(startserver)
		config['JackettUpdate']['autoupdate'] = str(autoupdate)
	with open('config.ini', 'w') as configfile:
		config.write(configfile)
except Exception as e:
	print("EmbyUpdate: Couldn't write to the config file.")
	print("EmbyUpdate: Here's the error we got -- " + str(e))
	sys.exit(1)
	

print("")
print("Config written to file!")
print("")


