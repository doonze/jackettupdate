#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# JackettUpdate
###############################################################################################
# This script can be used to to keep Jackett for Linux automatically up to date.              #
# It is setup for the X64 and ARM versions of Linux. If your distro uses systemd then         #
# this script has logic that can stop and start the server if needed. If you don't have       #
# systemd then if you want the server stopped and started by the script you'll need to        # 
# modify the commands as needed.                                                              #
# Should work with both python 2.7 and all flavors of 3.                                      #
###############################################################################################

# Sets the version # for the command line -v/--version response
versionnum = "2.0 Beta"
app = "JackettUpdate: "

if __name__ == "__main__":
    import sys
    import os
    import time
    import argparse
    from configparser import ConfigParser
    import configparser
    from timeit import default_timer as timer
    
    # First we're going to force the working path to be where the script lives
    os.chdir(sys.path[0])

    # Just to make python happy
    returncode = 0

    # This sets up the command line arguments
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

    # Here we update the config file if the user used the command line argument
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
        quit()


        # Now well try and update the app if the user chose that option
    from configread import appupdate

    if appupdate == 'True':
        import selfupdate

    import mainupdate
