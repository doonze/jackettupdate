# JackettUpdate
A python script for automatically updating or even installing Jackett to the latest version on Linux distros.

This is a self fork of my EmbyUpdate script. These scripts can be forked to update just about any github Linux project, with some work.

Jackett has an auto-updater built in, but it never works for me. It causes Jackett to start failing till I re-install Jackett. I've raised tickets on it, but while it seems to be a known issue, the exact cause on some systems is unknown. Hence this script, that DOES work.

If you use this script, disable the auto-updater in Jackett. Do this by checking the Disable auto update box.

This script has been tested with python 2.7 and 3+. I suggest using python 3, it always tries python 3 commands first. If those fail it falls back to python 2 commands. In the end it doesn't matter, it runs the same on both. However if you run it with 3 there won't be behind the scenes exceptions happening. If you don't have 3, or have mapped 3 to python instead of python3 you may get some chatter from the app. It was tested and developed on Debian 10. I haven't tested it on any other distro but it should work fine on Ubuntu and Mint for sure, or any other Debian based distro. Honestly it should work on any Linux flavor, but your milage may vary.

* Backup your server before doing anything!!!

Some thoughts. This script assumes your running Jackett as a systemd service. If you're not, simply answer no to the stop/start server conifg options. As long as you feed it the right path, it will still update Jackett just fine. But you'll have to restart the server on your own. If you need to make changes to this script, select the config option in setup to disable the scripts autoupdating feature. Or fork it, or whatever works for you.

### File List

* jackettupdate.py - This is the main file and the only one that should be ran manually
* configread.py - A module for pulling config file data
* configupdate.py - A module called by the script on demand to create/update the conifg file
* customfunctions.py - A module lib containing a number of useful functions used throughout the script
* mainupdate.py - The module for updateing jackett itself
* selfupdate.py - The module for updateing the script to the latest github release
* changelog.txt - The...ermmm... changelog
* systemd/jackettupdate.service - An example systemd unit file for running Jackettupdae through systemd
* systemd/jackettupdate.timer - An example timer file for running Jackettupdate on a schdeule
* systemd/readme - A quick summary on how to use the systemd files

### Prerequisites 

For Debian and it's derivatives all you need is:
```
wget
```
and these:
```
python or python3 (optional but highly suggested)
requests (pip install requests)
```

### Getting Started

You will need to have root/sudo/admin access to your server to use all this scripts functions. It won't have access to restart your Jackett server otherwise. If your user has access to the directory where Jackett is installed, it WILL update Jackett, it just can't stop and start the server to pick up the changes. You can choose to select options to not stop/start the server and do it yourself if you wish however.

Download the release .zip of your choice from my github. Unzip the files into a directory you have full access to. I suggest a directory in your home directory called jackettupdate. The very first time you run the script it will tell you that you have to run the config first. You'll have to run the following command and answer a few questions. Hitting enter on all but the first question will setup the defaults.

```
sudo python embyupdate.py --config
```
Here's the config options questions, all are required:

```
[1] Linux X64
[2] Linux ARM32
[3] Linux ARM64
Choose your distro by number or C to cancel update [?]:
```
Just choose your distro from the list, or choose c to cancel and not create/update the config file nor install/update Emby.

```
Root filepath to install Jackett? (Suggest /opt/. The Jackett tarball automatically creates a Jackett directory) [/opt/]:
```
Here you choose where to install/update Jackett. You MUST use the trailing /. (So /opt/ not /opt) or the script will fail. I could add logic to idiot proof this, but just follow instructions! Choose the ROOT path where you want Jackett installed, the tar file from Jackett github already has the /Jackett path built into it. If you choose /opt/ in other words here, Jackett will be installed to /opt/Jackett.

```
Name of systemd Jackett service? This is the name it runs on through systemd [ex. jackett]:
```
Here you enter the name of your Jackett service running in systemd. If you don't have one, and are starting and stopping the server in a different way it doesn't matter what you enter here. Just disable server stop/start below. You can use either the short service name (ex. jackett) or the long service name (ex. jackett.service) systemd doesn't care.


```
Do we need to manually stop the server to install? (Likely only needed for Arch.) [Y/n]: 
```

Just hit enter as by default we want to stop the server before updating. Only exception is if you don't have root access. Default is Yes.

```
Do we need to manually start the server after install? [Y/n]:
```
Just hit enter here as normally we'll want to restart the server after an update. Only exception is if you don't have root access. Default is Yes.

```
Keep EmbyUpdate (this script) up to date with latest version? [Y/n]
```

Defalut is yes. Unless you have a reason you don't want to keep the script updated, just hit enter. This will only update to Stable releases, beta releases will be ignored. I have no desire to change this behavior as I don't plan on keeping an up to date beta version. Only time I'll release beta's is if I'm doing major changes that need testing.

## It takes two runs for script updates to take effect. It does update the script (this program) during the first run, but as the script is already running during the update the changes are not implimented. The next time the script is called it will be running on the updated code. I have an idea on how to correct this behavior, but the need hasn't justified the complete code overhaul yet. The updated script will run the next day. So updates are delayed a day worst case senerio.

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

The last question will show you all the config options you have selected, and will ask you to type CONFIRM (all caps, just like that) or c to cancel the config creation/update. Typing CONFIRM (all caps) will move on to installing/updating Emby, cancel will discard all changes and stop the install.

You can invoke the config interface at any time with -c or --config, any changes you choose will be updated and the installer ran. After inital creation you'll only have need to rerun it if you want to change something. Otherwise normal usage is listed below.

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

Script sudo/root to be able to install packages and Stop/Start the server if needed. You can of course leave off the sudo if your already root.

### **I however suggest running it as a cron job as root.** 

See deployment section for cron example

### Supported Linux Distros
```
Should work out of the box on any Linux running Systemd. 
```


### Script Logic Flow

1. Script will test to see if config file exist. If it doesn't it will notify user they must run the config creator and exit. Once the config has been setup the script will move on to installing the latest Jackett version. 

2. Script will pull the latest stable version from Jackett's github page. Once it finds the most recent version it will stop searching the API and move on with that version. If it encouters any errors pulling from the page it will exit the script letting you know it failed and will try to tell you why.

3. Once it has pulled the latest version number it will test to see if that is the most recent version installed. 
  
 * The script keeps track of versions after the first install. However it will always try and update/install the server to the latest version the first time the script is run. This is for both Jackett AND the App itself. It will overwrite the JackettUpdate app itself with the latest version if updating it was selected in options. So I've you've made changes keep that in mind! Every other future run should be normal.
    
4. The script will start the upgrade now, first checking to see if your settings ask it to stop the server. As written this will only work on systemd systems, but the commands can be changed in the code as needed. 

5. The script will download the newest tar file from Jackett github. It will then run tar on the downloaded file in the ROOT directory you entered during setup. Set /opt/ and not /opt/Jackett for example, as Jackett tars already have the /Jackett dir built in.
   
   The app itself also checks for a more recent version. If it finds one it downloads the .zip file from my github releases, unzips it      in the current working directory, and then deletes the .zip to keep things nice and tidy. It will also mark the embyupdate.py file as    executable. Not needed, but I can so I did.
   
6. Lastly, if everything has gone ok with no errors, the script will write the newly installed version numbers into the config file.


## Deployment

Download, copy, git, svn, or use any other way you know to get the script on your box. An easy way is to download the source .zip in releases and unzip in in the desired directory (suggested way). I created a directory just for this script.

ALL FILES MUST REMAIN IN THE SAME DIRECTORY! Everything it does happens in the directory embyupdate.py lives in. If you move anything, delete anything, or rename anything your going to have issues. The script knows what directory it's in and behaves accordingly. You can move it anywhere, but you must move ALL FILES.

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
