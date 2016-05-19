#!/bin/bash
###########
# Version: 1.2
#
# Simple script to copy files from the download directory and transfer to another directory, Cleans up the left over files
# Made for usage with Sonar on a ChmuraNet Machine by default, Path names can simply be changed.
#
# https://github.com/halo779/AssortedSeedboxScripts
###########

torrentid=$1
torrentname=$2
torrentpath=$3

testdir="sonarrtmp"

if [[ "$torrentpath" =~ $testdir ]]
then
        echo "Torrent Details: " $torrentname $torrentpath $torrentid  >> ~/hard.log
        cp -R "$torrentpath/$torrentname" "/home/owner/completed/" #could use -l for hardlinking
        for f in $(find "/home/owner/completed/$torrentname/" -name '*.rar' -or -name '*.r00'); do unrar e -y $f "/home/owner/completed/"; done
        for f in $(find "/home/owner/completed/$torrentname/" -name '*.rar' -or -name '*.r??' -or -name '*sample*' -or -name 'Sample' -or -name '*.nfo' -or -name '*.sfv'); do rm -R $f; done #Careful with the -R
fi
