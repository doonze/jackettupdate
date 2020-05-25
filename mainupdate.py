import sys
import os
import json
import requests
import os.path
import time
import subprocess
from configparser import ConfigParser
import configparser
from timeit import default_timer as timer
from customfunctions import get_file, time_stamp, display_time, tar_extract
from jackettupdate import app
from configread import installbeta, distro, installpath, currentversion, appupdate, serverstart, servicename, serverstop

updatestart = timer()

# First we're going to force the working path to be where the script lives
os.chdir(sys.path[0])

# Sets up the config system
config = configparser.ConfigParser()

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
        print(time_stamp() + "JackettUpdate: We didn't get an expected response from the github api, script is exiting!")
        print(time_stamp() + "JackettUpdate: Here's the error we got -- " + str(e))
        sys.exit()

##########################################################################################################
# This block is just setting up the variables for your selected distro. These can be updated as needed.  #
##########################################################################################################

# Linux AMD64 **************************
if distro == "Linux X64":
    downloadurl = "https://github.com/Jackett/Jackett/releases/download/" + onlineversion + "/Jackett.Binaries.LinuxAMDx64.tar.gz" 
    installfile = installpath + "Jackett.Binaries.LinuxAMDx64.tar.gz"
    installcmd = "tar -C " + installpath + " -zxf " + installpath + "Jackett.Binaries.LinuxAMDx64.tar.gz"
    FileName = "Jackett.Binaries.LinuxAMDx64.tar.gz"
#***************************************

# Linux ARM32 **************************
if distro == "Linux ARM32":
    downloadurl = "https://github.com/Jackett/Jackett/releases/download/" + onlineversion + "/Jackett.Binaries.LinuxARM32.tar.gz"
    installfile = installpath + "Jackett.Binaries.LinuxARM32.tar.gz"
    installcmd = "tar -C " + installpath + " -zxf " + installpath + "Jackett.Binaries.LinuxARM32.tar.gz"
    FileName = "Jackett.Binaries.LinuxARM32.tar.gz"
#***************************************

# Linux ARM64 ***************************
if distro == "Linux ARM64":
    downloadurl = "https://github.com/Jackett/Jackett/releases/download/" + onlineversion + "/Jackett.Binaries.LinuxARM64.tar.gz"
    installfile = installpath + "Jackett.Binaries.LinuxARM64.tar.gz"
    installcmd = "tar -C " + installpath + " -zxf " + installpath + "Jackett.Binaries.LinuxARM64.tar.gz"
    FileName = "Jackett.Binaries.LinuxARM64.tar.gz"
#***************************************

###################################################################################################
# End distro setup block. End of user configable sections. Don't change anything below this line. #
###################################################################################################


# Ok, we've got all the info we need. Now we'll test if we even need to update or not.

onlinecurrentversion = (onlineversion + "-" + versiontype)

if str(onlinecurrentversion) in str(currentversion):
    updateend = timer()
    totalupdatetime = display_time(updateend - updatestart)
    # If the latest online version matches the last installed version then we let you know and quit Jackett update
    print("{}We're up to date! Current and Online versions are at {}. Check took {}.".format(time_stamp(app), onlinecurrentversion, totalupdatetime))
    print("")  
else:
    # If the online version DOESN'T match the last installed version we let you know what the versions are and start updating
    print(time_stamp() + "JackettUpdate: Most recent online version is " + onlinecurrentversion + " and current installed version is " + currentversion + ". We're updating Jackett.")
    print(time_stamp() + "JackettUpdate: Starting update......")

    try:

        BadCode = False

        # This will stop the server on a systemd distro if it's been set to true
        if serverstop == "True":
            stopreturn = subprocess.call("systemctl stop " + servicename,shell=True)
            print(time_stamp(app) + "Server " + servicename + " being stopped...")
            if stopreturn > 0:
                print("{}Server Stop failed! It didn't exist, wasn't running, or we had some other issue.".format(time_stamp(app)))
            
        # Here we download the tar file
        if "notused" not in downloadurl:
            print(time_stamp(app) + "Download started...")
            print(get_file(downloadurl, installpath, app))
            print(time_stamp(app) + "Download Finished.")

        # Next we install it with tar then remove the install file
        if "notused" not in installcmd:
            print(time_stamp(app) + "Install/Update started...")
            ReturnResult = tar_extract(FileName, installpath, app=app, RemoveFile=True)

            # Now we test the returned dictionary for a return code and react accordingly
            if ReturnResult["ReturnCode"] == 0:
                print("{}".format(ReturnResult["result"])) 
            else:
                BadCode = True
                print("{}".format(ReturnResult["result"]))
                       
            print(time_stamp(app) + "Install/Update finished.")

        # This will restart the server if using systemd if set to True above
        if serverstart == "True":
            startreturn = subprocess.call("systemctl start " + servicename,shell=True)
            print(time_stamp(app) + "Server being Started.")
            if startreturn > 0:
                print("{}Server start failed. Non-critical to update but server may not be running. Investigate.".format(time_stamp(app)))
                
            # Lastly we write the newly installed version into the config file if the return codes were ok
        try:
            if BadCode == False:
                config.read('config.ini')
                config['SERVER']['jackettversion'] = onlinecurrentversion
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                updateend = timer()
                totalupdatetime = display_time(updateend - updatestart)
                print(time_stamp() + "JackettUpdate: Updating to version " + onlinecurrentversion + " finished! Update took " + totalupdatetime + ". Script exiting!")
                print('')            
            else:
                print("{}Install failed! See logs! Version not updated!".format(time_stamp(app)))
        except Exception as e:
            print("{}Couldn't write into the config file!".format(time_stamp(app)))
            print("{}Here's the error we got -- {}".format(time_stamp(app), e))        

    except Exception as e:
        print(time_stamp() + 'JackettUpdate: Something failed in update. No update done, script exiting')
        print(time_stamp() + "JackettUpdate: Here's the error we got -- " + str(e))

quit()