from configparser import ConfigParser
import configparser
import os
import sys

# Set to path to current location
os.chdir(sys.path[0])


# Here we pull the main config params.
try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    distro = config['DISTRO']['installdistro']
    installbeta = config['DISTRO']['releaseversion']
    installpath = config['SERVER']['installpath']
    servicename = config['SERVER']['servicename']
    serverstop = config['SERVER']['stopserver']
    serverstart = config['SERVER']['startserver']
    currentversion = config['SERVER']['jackettversion']
    appupdate = config['JackettUpdate']['autoupdate']
    appversion = config['JackettUpdate']['version']
    
except Exception as e:
    print("JackettUpdate: Couldn't pull config info!!!")
    print("JackettUpdate: Here's the error we got -- " + str(e))
    quit()