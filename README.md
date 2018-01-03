# 2085-jevois-vision-suite

A fork of 2073's Jevois vision programming. The intent of this project is to provide similar functionality to the original with a slightly modified methodology. 

Rather than the traditional HSV filtering approach, this program uses the Green-Red approach outlined here https://www.chiefdelphi.com/forums/showthread.php?p=1713557#post1713557
As outlined in the post this method allows the camera to be set with normal exposure settings and used as a driver aid when not being used for targeting. 
To facilitate this the tuning script was modified to remove HSV options and add ratio filtering.