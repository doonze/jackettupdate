# JackettUpdate
A python script for automatically updating or even installing Jackett to the latest version on Linux distros.

This is a self fork of my EmbyUpdate script. These scripts can be forked to update just about any github Linux project, with some work.

Jackett has an auto-updater built in, but it never works for me. It causes Jackett to start failing till I re-install Jackett. I've raised tickets on it, but while it seems to be a known issue, the exact cause on some systems is unknown. Hence this script, that DOES work.

If you use this script, disable the auto-updater in Jackett. Do this by checking the Disable auto update box.

This script has been tested with python 2.7 and 3+. I suggest using python 3 however, as 2 is at end of life support. It was tested and developed on Debian 10. I haven't tested it on any other distro but it should work fine on Ubuntu and Mint for sure, or any other Debian based distro. Honestly it should work on any Linux flavor, but your milage may vary.

Some thoughts. This script assumes your running Jackett as a systemd service. If you're not, simply answer no to the stop/start server config options. As long as you feed it the right path, it will still update Jackett just fine. But you'll have to restart the server on your own. If you need to make changes to this script, select the config option in setup to disable the scripts autoupdating feature. Or fork it, or whatever works for you.

### File List

* jackettupdate.py - This is the main file and the only one that should be ran manually
* changelog.txt - The...ermmm... changelog
* README.MD - This file
* LICENSE - Github legal stuff
* .gitignore - Included just in case you might want to contribute. Will ignore the correct files
* moduals/configread.py - A module for pulling config file data
* moduals/configupdate.py - A module called by the script on demand to create/update the conifg file
* moduals/customfunctions.py - A module lib containing a number of useful functions used throughout the script
* moduals/mainupdate.py - The module for updateing jackett itself
* moduals/selfupdate.py - The module for updateing the script to the latest github release
* systemd/jackettupdate.service - An example systemd unit file for running Jackettupdae through systemd
* systemd/jackettupdate.timer - An example timer file for running Jackettupdate on a schdeule
* systemd/readme - A quick summary on how to use the systemd files

### Prerequisites 

For Debian and it's derivatives (all linux really) all you need is:
```
python or python3 (optional but highly suggested)
```
For python modules:

```
requests (pip install requests)
builtins (maybe? I had to install it for python 2. pip install builtins)
```

### Getting Started

You will need to have root/sudo/admin access to your server to use all this scripts functions. It won't have access to restart your Jackett server otherwise. If your user has access to the directory where Jackett is installed, it WILL update Jackett, it just can't stop and start the server to pick up the changes. You can choose to select options to not stop/start the server and do it yourself if you wish however.

I suggest installing this script to /usr/local/bin in it's own directory (like jackettupdate). Just to keep with the linux hiarchy standards. I then sys link that directory to my home directory, and set permission accordingly. If you don't have root access then just install in your home directly and be done with it.

Once you have the script installed, I suggest running the below command as your user, this creates the config file with your permissions so if you ever have need to manually change it you have access. This will just run the config creator.
```
python embyupdate.py -c
```
Here's the config options questions, all are required:

```
[1] Linux X64
[2] Linux ARM32
[3] Linux ARM64
Choose your distro by number or C to cancel update [?]:
```
Choose your distro from the list, or choose c to cancel and not create/update the config file..

```
Root filepath to install Jackett? (Suggest /opt/. The Jackett tarball automatically creates a Jackett directory) [/opt/]:
```
Here you choose where to install/update Jackett. Choose the ROOT path where you want Jackett installed, the tar file from Jackett github already has the /Jackett path built into it. If you choose /opt/ in other words here, Jackett will be installed to /opt/Jackett.

```
Name of systemd Jackett service? This is the name it runs on through systemd [ex. jackett]:
```
Here you enter the name of your Jackett service running in systemd. If you don't have one, and are starting and stopping the server in a different way it doesn't matter what you enter here. Just disable server stop/start below. You can use either the short service name (ex. jackett) or the long service name (ex. jackett.service) systemd doesn't care.


```
Do we need to manually stop the server to install? [Y/n]: 
```

Just hit enter as by default we want to stop the server before updating. Only exception is if you don't have root access. Default is Yes.

```
Do we need to manually start the server after install? [Y/n]:
```
Just hit enter here as normally we'll want to restart the server after an update. Only exception is if you don't have root access. Default is Yes.

```
Keep JackettUpdate (this script) up to date with latest version? [Y/n]
```

Defalut is yes. Unless you have a reason you don't want to keep the script updated, just hit enter. This will only update to Stable releases, beta releases will be ignored. I have no desire to change this behavior as I don't plan on keeping an up to date beta version. Only time I'll release beta's is if I'm doing major changes that need testing.

## The selfupdate runs before the Jackett update, so the Jackett update portion will ALWAYS run with any new updates. The selfupdate portion will not run with any new updates till it's NEXT run. I have it on my todo list to get python to update, then rerun the entire script with any updates. Shouldn't ever been an issue really, it's more I want to do it to do it.

```
Choices to write to config file...
Linux distro version to update: Linix X64
/opt/ set as Jackett install root directory
The chosen version for install is: Stable
Server will NOT be manually stopped on install.
Server will NOT be manually started after install.
Script (JackettUpdate) will be automatically updated!

Please review above choices and type CONFIRM to continue or c to cancel update and install! [CONFIRM/c]
```

The last question will show you all the config options you have selected, and will ask you to type CONFIRM (all caps, just like that) or c to cancel the config creation/update. Typing CONFIRM (all caps) will move on to installing/updating Emby unless called but the -c option, cancel will discard all changes and stop the install.

You can invoke the config interface at any time with -c or --config, any changes you choose will be updated and used the next time the script runs. After inital creation you'll only have need to rerun it if you want to change something. Otherwise normal usage is listed below.

Usage is: 
```
sudo python jackettupdate.py 
```
or
```
sudo python3 jackettupdate.py (suggested)
```
or if you have made it executable (see Deployment below)
```
sudo ./jackettupdate.py
```

Also, there are a few command line arguments you can use:

```
-c/--config = config creator/updator
-v/--version = display current version
-h/--help = displays help
```

Run the Script as sudo/root to be able to install packages and Stop/Start the server if needed. You can of course leave off the sudo if your already root.

### **I however suggest running it as a cron job as root.** 

See deployment section for cron example

### Supported Linux Distros
```
Should work out of the box on any Linux running Systemd. 
```


### Script Logic Flow

1. Script will test to see if config file exist. If it doesn't it will run the config updater. Once the config has been setup the script will move on to installing the latest Jackett version. 

2. Script will check for any updates to the script itself from my github, download it if there is one, and install the changes.

3. Script will pull the latest stable version from Jackett's github page. Once it finds the most recent version it will stop searching the API and move on with that version. If it encouters any errors pulling from the info from github it will exit the script letting you know it failed and will try to tell you why.

4. Once it has pulled the latest version number it will test to see if that is the most recent version installed. 
  
 * The script keeps track of versions after the first install. However it will always try and update/install the server to the latest version the first time the script is run. This is for both Jackett AND the App itself. It will overwrite the JackettUpdate app itself with the latest version if updating it was selected in options. So if you've made changes keep that in mind! Every other future run should be normal.
    
5. The script will start the upgrade now, first checking to see if your settings ask it to stop the server. As written this will only work on systemd systems, but the commands can be changed in the code as needed. 

6. The script will download the newest tar file from Jackett github. It will then untar the downloaded file in the ROOT directory you entered during setup. Remember to use /opt/ and not /opt/Jackett as ROOT directory for install, as Jackett tars already have the /Jackett directory built in.

7. Lastly, if everything has gone ok with no errors, the script will write the newly installed version numbers into the config file.

I didn't list it in the steps, but after it downloads and installs any updates it selfcleans the install files to keep things nice and tidy.


## Deployment

Download, copy, git, svn, or use any other way you know to get the script on your box. An easy way is to download the source .zip in releases and unzip in in the desired directory (suggested way). I created a directory just for this script.

ALL FILES MUST REMAIN IN THEIR DIRECTORIES! The directory structure matters! If you move anything, delete anything, or rename anything your going to have issues. The script knows what directory it's in and behaves accordingly. You can move it anywhere, but you must move ALL FILES in the structure as installed.

Make the job executable by running this command on the script (optional)
```
sudo chmod u+x jackettupdate.py 
```
Then you can run the script with a simple (optional)
```
sudo ./jackettupdate.py
```
Or if you placed it in your $PATH (really optional! And untested)
```
sudo jackettupdate.py
```

As stated above you must either be root or use sudo because the script calls privileged Linux commands. I also highly suggest running the script through cron as root.

# I now suggest running Jackett as a systemd service as apposed to running it with cron. The linux world has moved on from 30 year old cron to systemd, we might as well leverage it and learn to love systemd, it's not going anywhere. There is a readme in the systemd directory the install creates with instructions to setup Jackett as a systemd service. I've even included the files you'll need.

Example CRONTAB entry:
```
35 12   * * *    root  /usr/bin/python3 /path/to/jackettupdate/embyupdate.py >> /path/to/jackettupdate/embyupdate.log 2>&1
```
That runs the script every day at 12:35 and creates a log file in the location of my choice. I use my script location.

However, if your user has sudo access without a password, you could update the commands in the script by apending
```
sudo
```
in front of them. (I mean the systemd commands and the package install command inside the script itself). Then you could run the script as normal from your user.
```
./embyupdate.py
```

## Authors

* Justin Hopper - **Creator**
