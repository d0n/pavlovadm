pavlovadm
=========


Description
-----------
Due to the use of the python "inquirer" library pavlovadm isn't compatible to windows currently. You can either use Linux itself or the
Windows-Subsystem for Linux which is available in Windows 10 through the "Apps and Features" -> "Programs and Features"
(upper right Corner) -> "Activate or deactivate Windos-Features" (upper left corner) -> Windows-Subsystem for Linux (set hook).


Installation
------------
You need to have python appropriate to your OS distribution. Get it from <https://python.org/>

``pip install pavlovadm``


Credits
-------
  * Mark Dey - a PAVLOV developer which saved alot of time when the rcon interface wasn't updated to full functionality


Troubleshoot
------------
I would advise everyone to not open the RCON port(s) to public internet since the auth mecanism seems to be some centuries old -
it uses md5 as hashing algorithm and i am not sure if it uses encryption and if i doubt it's descent. To make it quick i would
propose to place the tool on the server which is most probably a linux system which would fix the library dependecy problem as well.
If so you also most possibly do have SSH enabled which even allows to bind a single command to a ssh-key. I would propose the following
setup:

``ssh-keygen -t ed25519`` # creates nice small keys with strong security

``echo "command=/path/to/pavlovadm $(cat ~/.ssh/id_ed25519.pub)" >~/.ssh/authorized_keys`` # set path to pavlovadm and authorized_keys file

You then simply can connect to that server using ``ssh -i ~/.ssh/ed_25519 user@host`` to be dropped into the rcon tool using the encrypted connection
of SSH. The RCON ports don't need to be opened to the internet any more though.
