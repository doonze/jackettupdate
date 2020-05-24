import time
import os
import requests
import sys
import tarfile
from timeit import default_timer as timer
from requests.exceptions import HTTPError

#Setting up a way to display time in human readable format
def display_time(seconds, granularity = 2):
    intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),    
    )
    result = []
    if seconds < 1:
        return "less than a second"
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(round(value), name))
    return ', '.join(result[:granularity])
#***********************************************************

# This is a simple timestamp function, created so each call would have a current timestamp
def timestamp(app = ""):
    ts = time.strftime("%x %X", time.localtime())
    return (ts + " - {}".format(app))
#******************************************************************************************

# Pass a file name (if in same directory as script) or a file name and a path
# example: sizeoffile("file.py") or sizeoffile("file.py", "/path/to/file/")
def sizeoffile(File, Path = sys.path[0]):
    if Path[-1] != "/":
        Path = Path + "/"
    pathtofile = Path + File
    result = sizeof(os.path.getsize(pathtofile))
    return result

# If passed a size in bytes it will convert to human readable sizes
def sizeof(num, suffix='B'):   
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
#***************************************************************************************************

# Used to download files. Feed it a url, and optionally a save path, and it will download the file
# If not save path is given, it will default to the same path as the calling script
def getfile(url, SavePath = sys.path[0],app=""):
    
    try:
        dlstart = timer()
        # Here we pull in the file and save it to returnedfile
        returnedfile = requests.get(url)
        
        # Next we'll check to see if the download was successful, if not we raise an exception handled below    
        returnedfile.raise_for_status()

        # Now we're going to figure out the file name from the URL. First we figure out the index of the last
        # / in the string using rindex, that gives us the postion of the /, so then we add + 1 to get the first
        # part of the filename, then we split the string there only keeping the filename.
        index = (url.rindex('/') + 1)
        FileName = str(url[index:])

        # Just to make life easy, we'll test if the path already ends in a / or not. If it doesn't we'll add one
        if SavePath[-1] != "/":
            SavePath = SavePath + "/"

        # We then figure out the save path either from the default script location or a provided path.       
        fullfilepath = "{}{}".format(SavePath, FileName)

        # Next we open the file in the save location, then write the file there
        open(fullfilepath, "wb").write(returnedfile.content)

        total_dl_time = display_time(timer() - dlstart)
        # All that's left is to return the results to the user
        dlresults = timestamp(app) + "File:{} Size:{} was downloaded taking {}".format(FileName, sizeoffile(FileName, SavePath), total_dl_time)
        
    except HTTPError as http_err:
        return  timestamp(app) + "Download Failed! Condition code was: {}".format(http_err)
    except Exception as err:
        return  timestamp(app) + "Get File Error! Download worked, error in writing file? Error code was: {}".format(err)
    return dlresults
#*************************************************************************************************************************************

# Function for extracing tar files ***************************************************************************************************
# Jackett uses "r:gz", as do most tars it seems I've used, so that's the default 
# Here are the list of modes
# 'r' or 'r:*' Open for reading with transparent compression (recommended)
# 'r:' Open for reading exclusively without compression
# 'r:gz' Open for reading with gzip compression
# 'r:bz2' Open for reading with bzip2 compression
# 'a' or 'a:' Open for appending with no compression. The file is created if it does not exist
# 'w' or 'w:' Open for uncompressed writing
# 'w:gz' Open for gzip compressed writing
# 'w:bz2' Open for bzip2 compressed writing

def tar_extract(File, Path=sys.path[0], Mode="r:gz", RemoveFile=False, app=""): 

    try:
        # Just to make life easy, we'll test if the path already ends in a / or not. If it doesn't we'll add one
        if Path[-1] != "/":
            Path = Path + "/"
        
        # Then we set extractedsize to just to not get a null excpetion 
        extractedsize = 0

        #Start the timer for keeping track of how long the extract took
        startextract = timer()

        #Then we open the tar file for reading
        tar = tarfile.open(Path + File, Mode)
        
        #Now we loop through the tar to get the size it will be once extracted
        for tarinfo in tar:
          extractedsize = extractedsize + tarinfo.size
        
        # Now we extract opened tar file to the set path, then close the tar file
        tar.extractall(Path)
        tar.close()

        #Before we (optionally) remove the file, we'll get it's size
        filesize = sizeoffile(File,Path)

        #Option to remove the file after installing (Default is False)
        if RemoveFile == True:
            RemoveResult = remove_file(File, Path)
        else:
            RemoveResult = "{} not removed".format(Path + File)
        # We end the extract process timer 
        endextract = timer()

        # Now we figure out how long it took to extract, the extracted size in a human readable form, 
        # and write the return string of the results        
        extracttime = display_time(endextract - startextract)
        extractedsize = sizeof(extractedsize)

        # Now we build a dictionary to hold the return results
        result = "{}File: {} Tar Size: {} Extracted Size: {} and was extracted in {}".format(timestamp(app), File, filesize, extractedsize , extracttime)
        result = result + "\n{}{}".format(timestamp(app), RemoveResult)
        ReturnCode = 0
        Results = {
            "result" : result,
            "ReturnCode" : ReturnCode
        }

    except Exception as err:
        result = "Tar Extract Error! Error code was: {}".format(err)
        ReturnCode = 1
        Results = {
            "result" : result,
            "ReturnCode" : ReturnCode
        }
        return Results
        
    return Results
#***********************************************************************************************************************************


# Function to remove a file in a given path **************************************************************
def remove_file(File, Path = sys.path[0]):
    
    try:
        # First we make sure the path has a / on the end
        if Path[-1] != "/":
            Path = Path + "/"

        # Now we build the path to delete the file
        FullPath = (Path + File)

        # We'll check to make sure the file exist before removing it, and let the user know if it doesn't
        if os.path.exists(FullPath):
            os.remove(FullPath)
        else:
            return "Delete error: {} does not exist. Nothing removed.".format(FullPath)

    except Exception as e:
        return "Remove File exception! Here's the error: {}".format(e)

    return "{} removed.".format(FullPath)
#**********************************************************************************************************