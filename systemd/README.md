I've included these copies of my working systemd files. This isn't by any means required
but systemd is the way the linux community has decided to go, so might as well get up
with the times.

On at least a Debian based systems the path to place these files is:

```
/lib/systemd/system/
```

I don't know if that true of all distro, so if you're unsure Google is your friend!

I've included my suggested pathing in these files, if you choose to place the scripts
somewhere else you'll need to adjust accordingly in the service file. If you want to 
change the time it runs, adjust the .timer file. 

If you're use my pathing, once you've copied these files over to systemd all you have to do
is run the following two commands:

```
#systemctl enable jackettupdate.timer
#systemctl start jackettupdate.timer
```

and if you want to see that they indeed are working
```
#systemctl list-timers
```


