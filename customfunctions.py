import time
import os
import requests
import sys
from timeit import default_timer as timer
from requests.exceptions import HTTPError

#Setting up a way to display time in human readable format
def display_time(seconds, granularity=2):
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
def timestamp(app=""):
    ts = time.strftime("%x %X", time.localtime())
    return ("<" + ts + "> {}".format(app))
#******************************************************************************************

# Pass a file name (if in same directory as script) or a file name and a path
# example: sizeoffile("file.py") or sizeoffile("file.py", "/path/to/file/")
def sizeoffile(File, Path=sys.path[0]):
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
def getfile(url, SavePath=sys.path[0]):
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
        dlresults = timestamp() + "File:{} Size:{} was downloaded taking {}".format(FileName, sizeoffile(FileName, SavePath), total_dl_time)
        
    except HTTPError as http_err:
        return  timestamp() + "Download Failed! Condition code was: {}".format(http_err)
    except Exception as err:
        return  timestamp() + "Get File Error! Dowload worked, error in writing file? Error code was: {}".format(err)
    return dlresults
#*************************************************************************************************************************************