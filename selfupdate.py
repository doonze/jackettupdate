#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# This program is used can called by the main program to update the app itself if needed
# JackettUpdate selfupdate file

app = "JackettUpdate(self): "
import sys
import os
import json
import requests
import os.path
import time
import pprint
import zipfile
import subprocess
from timeit import default_timer as timer
from configparser import ConfigParser
import configparser
from customfunctions import time_stamp, get_file, display_time, remove_file
from configread import appversion
print(" Self update started")

selfupdatestart = timer()
# Sets up the config system
config = configparser.ConfigParser()

# I don't use beta releases, but this is here just in case I do in the future
installbeta = False

# We're going to force the working path to be where the script lives
os.chdir(sys.path[0])

# The github API of releases for app. This includes beta and production releases
url = "https://api.github.com/repos/doonze/jackettupdate/releases"

# Now we're just going to see what the latest version is! If we get any funky response we'll exit the script.
try:
    response = requests.get(url)
    updatejson = json.loads(response.text)
    # Here we search the github API response for the most recent version of beta or stable depending on what was chosen by the user
    for i, entry in enumerate(updatejson):
        if (installbeta == True):

            if entry["prerelease"] == True:
                onlineversion =  entry["tag_name"]
                versiontype = "Beta"
                break
        else:

            if entry["prerelease"] == False:
                onlineversion =  entry["tag_name"]
                versiontype = "Stable"
                break
except Exception as e:
    print(time_stamp(app) + "We didn't get an expected response from the github api, script is exiting!")
    print(time_stamp(app) + "Here's the error we got -- " + str(e))
    print(e)
    sys.exit()
    
# Download URL for my github page (app home page) and we'll set the name of the current zip file
downloadurl = "https://github.com/doonze/JackettUpdate/archive/" + onlineversion + ".zip" 
zfile = onlineversion + ".zip"

# Ok, we've got all the info we need. Now we'll test if we even need to update or not.
onlinefileversion = (onlineversion + "-" + versiontype)

if str(onlinefileversion) in str(appversion):    
    selfupdateend = timer()
    totalupdatetime = display_time(selfupdateend - selfupdatestart)
    # If the latest online version matches the last installed version then we let you know and move on
    print("{}App is up to date! Current and Online versions are at {}. Check took {}.".format(time_stamp(app), onlinefileversion, totalupdatetime))
else:
	# If the online version DOESN'T match the last installed version we let you know what the versions are and start updating
    print('')
    print(time_stamp(app) + "Most recent app online version is " + onlinefileversion + " and current installed version is " + appversion + ". We're updating JackettUpdate app.")
    print('')
    print("\n" + time_stamp(app) + "Starting self app update, installing to " + str(sys.path[0]) + "......")
    print('')

   	# Here we download the zip to install          
    print(get_file(downloadurl, app=app))
    
	# Next we unzip and install it to the directory where the app was ran from
    with zipfile.ZipFile(zfile) as zip:
        for zip_info in zip.infolist():
            if zip_info.filename[-1] == '/':
                continue
            zipversion = onlineversion.replace("v", "")
            zip_info.filename = zip_info.filename.replace("jackettupdate-" + zipversion + "/", "")
            zip.extract(zip_info, '')

	# And to keep things nice and clean, we remove the downloaded file once unzipped
    print(remove_file(zfile, app=app))

    # now we'll set the app as executable
    st = os.stat("jackettupdate.py")
    os.chmod("jackettupdate.py", st.st_mode | 0o111)

	# Lastly we write the newly installed version into the config file
    try:
        # Now we're going to open the config file reader        
        config['JackettUpdate']['version'] = onlinefileversion
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        print(time_stamp(app) + "We couldn't write the installed version to the config file!")
        print(time_stamp(app) + "Here's the error we got -- " + str(e))
        quit()
    
    selfupdateend = timer()
    totalupdatetime = display_time(selfupdateend - selfupdatestart)

    print('')
    print("{} Updating to app version {} took {}.".format(time_stamp(app), onlinefileversion, totalupdatetime))

