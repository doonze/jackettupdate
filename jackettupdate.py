#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# JackettUpdate
# Sets the version # for the command line -v/--version response
versionnum = "1.4 Beta"
app = "JackettUpdate: "

import sys
import os
import json
import requests
import os.path
import time
import argparse
import subprocess
from configparser import ConfigParser
import configparser
from timeit import default_timer as timer
import datetime
from customfunctions import *


updatestart = timer()
# First we're going to force the working path to be where the script lives
os.chdir(sys.path[0])

# Just to make python happy
returncode = 0

# This sets up the comand line arguments
parser = argparse.ArgumentParser(description="An updater for Jackett",prog='jackettupdate')
parser.add_argument('-c','--config', action='store_true', help='Runs the config updater',required=False)
parser.add_argument('-v','--version', action='version', version='%(prog)s ' + versionnum,help='Displays version number')
args = parser.parse_args()

# If the user hasn't used the -c/--config command line argument this will test to see if the config file exist. If it doesn't
# it will prompt the user to run the config tool from the command line. This only needs done once.
if args.config == False:
    if not os.path.isfile("config.ini"):
        print("")
        print("Config file doesn't exist! Likely this is your first time running the script. Starting configuration manager.")
        print("")
        import configupdate

# Here we try python3 configparser import. If that fails it means user is running python2. So we import
# the python2 ConfigParser instead
try:
    config = configparser.ConfigParser()
    if args.config == True:
        print("")
        print("Config update started....")
        print("")
        import configupdate
except Exception as e:
    print("JackettUpdate: Couldn't call the configupdater.")
    print("JackettUpdate: Here's the error we got -- " + str(e))
    sys.exit()

# Here we test to see if the called subprocess above got a return code. If the return code is 1 then
# the entire process is exited and no updates will be installed. This is triggered by one of the two
# cancel prompts in the configupdate.py script
if returncode == 1:
    sys.exit()

# Now we're going to open the config file reader
config.read('config.ini')

###############################################################################################
# This script can be used to to keep Jackett for Linux automatically up to date.              #
# It is setup for the X64 and ARM versions of Linux. If your distro uses systemd then         #
# this script has logic that can stop and start the server if needed. If you don't have       #
# systemd then if you want the server stopped and started by the script you'll need to        # 
# modify the commands as needed.                                                              #
# Should work with both python 2.7 and all flavors of 3.                                      #
###############################################################################################

# Here we pull the main config params.
try:
    distro = config['DISTRO']['installdistro']
    installbeta = config['DISTRO']['releaseversion']
    installpath = config['SERVER']['installpath']
    servicename = config['SERVER']['servicename']
    serverstop = config['SERVER']['stopserver']
    serverstart = config['SERVER']['startserver']
    appupdate = config['JackettUpdate']['autoupdate']
except Exception as e:
    print("JackettUpdate: Couldn't pull config info!!!")
    print("JackettUpdate: Here's the error we got -- " + str(e))
    quit()

# The github API of releases for Jackett. This includes beta and production releases
url = "https://api.github.com/repos/Jackett/Jackett/releases"

# Now we're just going to see what the latest version is! If we get any funky response we'll exit the script.
try:
    response = requests.get(url)
    updatejson = json.loads(response.text)
    # Here we search the github API response for the most recent version of beta or stable depending on what was chosen 
    #above. 
    for i, entry in enumerate(updatejson):
        if installbeta == 'Beta':

            if entry["prerelease"] == True:
                onlineversion =  entry["tag_name"]
                versiontype = "Beta"
                break
        elif installbeta == 'Stable':

            if entry["prerelease"] == False:
                onlineversion =  entry["tag_name"]
                versiontype = "Stable"
                break

        else:
            print("Couldn't determine release requested, value is " + installbeta)

except Exception as e:
        print(timestamp() + "JackettUpdate: We didn't get an expected response from the github api, script is exiting!")
        print(timestamp() + "JackettUpdate: Here's the error we got -- " + str(e))
        sys.exit()

##########################################################################################################
# This block is just setting up the variables for your selected distro. These can be updated as needed.  #
##########################################################################################################

# Linux AMD64 **************************
if distro == "Linux X64":
    downloadurl = "https://github.com/Jackett/Jackett/releases/download/" + onlineversion + "/Jackett.Binaries.LinuxAMDx64.tar.gz" 
    installfile = installpath + "Jackett.Binaries.LinuxAMDx64.tar.gz"
    installcmd = "tar -C " + installpath + " -zxf " + installpath + "Jackett.Binaries.LinuxAMDx64.tar.gz"
#***************************************

# Linux ARM32 **************************
if distro == "Linux ARM32":
    downloadurl = "https://github.com/Jackett/Jackett/releases/download/" + onlineversion + "/Jackett.Binaries.LinuxARM32.tar.gz"
    installfile = installpath + "Jackett.Binaries.LinuxARM32.tar.gz"
    installcmd = "tar -C " + installpath + " -zxf " + installpath + "Jackett.Binaries.LinuxARM32.tar.gz"
#***************************************

# Linux ARM64 ***************************
if distro == "Linux ARM64":
    downloadurl = "https://github.com/Jackett/Jackett/releases/download/" + onlineversion + "/Jackett.Binaries.LinuxARM64.tar.gz"
    installfile = installpath + "Jackett.Binaries.LinuxARM64.tar.gz"
    installcmd = "tar -C " + installpath + " -zxf " + installpath + "Jackett.Binaries.LinuxARM64.tar.gz"
#***************************************

###################################################################################################
# End distro setup block. End of user configable sections. Don't change anything below this line. #
###################################################################################################

# Now were going to pull the version from the config file
try:
    fileversion = config['SERVER']['jackettversion']
except Exception as e:
    print("JackettUpdate: Couldn't pull version info from the config file!")
    print("JackettUpdate: Here's the error we got -- " + str(e))
    quit()

# Ok, we've got all the info we need. Now we'll test if we even need to update or not.

onlinefileversion = (onlineversion + "-" + versiontype)
end = timer()
if str(onlinefileversion) in str(fileversion):
    # If the latest online version matches the last installed version then we let you know and exit
    print(timestamp() + "JackettUpdate: We're up to date!  Current and Online versions are at " + onlinefileversion + ".")
    if appupdate == "False":
        print("")  
else:
    # If the online version DOESN'T match the last installed version we let you know what the versions are and start updating
    print(timestamp() + "JackettUpdate: Most recent online version is " + onlinefileversion + " and current installed version is " + fileversion + ". We're updating Jackett.")
    print(timestamp() + "JackettUpdate: Starting update......")

    try:
        # This will stop the server on a systemd distro if it's been set to true above
        if serverstop == "True":
            stopreturn = subprocess.call("systemctl stop " + servicename,shell=True)
            print(timestamp(app) + "Server " + servicename + " being stopped...")
            if stopreturn > 0:
                print("{}Server Stop failed! It didn't exist, wasn't running, or we had some other issue.".format(timestamp(app)))
            
        # Here we download the package to install if used
        if "notused" not in downloadurl:
            print(timestamp(app) + "Download started...")
            print(getfile(downloadurl, installpath))
            print(timestamp(app) + "Download Finished.")

        # Next we install it if used
        if "notused" not in installcmd:
            print(timestamp(app) + "Install/Update started...")
            installreturn = subprocess.call(installcmd,shell=True)
            print(timestamp(app) + "Install/Update finished.")
            if installreturn > 0:
                print("{}Install failed! Exiting!".format(timestamp(app)))
                sys.exit()

        # And to keep things nice and clean, we remove the downloaded file once installed if needed
        if "notused" not in installfile:
            subprocess.call("rm -f " + installfile,shell=True)
            print(timestamp(app) + "Install file " + installfile + " removed.")

        # This will restart the server if using systemd if set to True above
        if serverstart == "True":
            startreturn = subprocess.call("systemctl start " + servicename,shell=True)
            print(timestamp(app) + "Server being Started.")
            if startreturn > 0:
                print("{}Server start failed. Non-critical to update but server may not be running. Investigate.".format(timestamp(app)))
                
            # Lastly we write the newly installed version into the config file
        try:
            config['SERVER']['jackettversion'] = onlinefileversion
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            print("JackettUpdate: Couldn't write into the config file!")
            print("JackettUpdate: Here's the error we got -- " + str(e))
            sys.exit()        
        updateend = timer()
        totalupdatetime = display_time(updateend - updatestart)
        print(timestamp() + "JackettUpdate: Updating to version " + onlinefileversion + " finished! Update took " + totalupdatetime + ". Script exiting!")

    except Exception as e:
        print(timestamp() + 'JackettUpdate: Something failed in update. No update done, script exiting')
        print(timestamp() + "JackettUpdate: Here's the error we got -- " + str(e))

# Now well try and update the app if the user chose that option
selfupdatestart = timer()
if appupdate == 'True':
    import selfupdate

print("*****************************************************************************")
quit()
