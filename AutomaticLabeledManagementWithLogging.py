#!/usr/bin/python
"""
Scripted automation of Deluge, Using deluge_framework.
This removes all torrents past a set value, which are fully downloaded and above a set ratio
Logging is also included in this, it is not required by could be of use

Collection of all my scripts are at my Github, https://github.com/halo779/AssortedSeedboxScripts
"""

from deluge_framework import filter_torrents
import logging
from logging.handlers import TimedRotatingFileHandler

__version__ = "1.1.0"


#Globals
TORRENTSLABLEDCOUNT = 0
TORRENTSREMOVED = 0
TORRENTSREMOVED = 0
TORRENTSPASSEDSEEDINGCONDITIONS = 0

#Logger Setup
#logging.basicConfig(level=logging.DEBUG) #For Console Debugging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = TimedRotatingFileHandler('AutoDLAutomaticManagement.log', when='M', interval=1, backupCount=52)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def torrentAction(torrent_id,torrent_info):
    global TORRENTSLABLEDCOUNT
    global TORRENTSREMOVED
    global TORRENTSREMOVED
    global TORRENTSPASSEDSEEDINGCONDITIONS
    if 'delugeLabel' in torrent_info['label']:
        TORRENTSLABLEDCOUNT+=1
        if long(torrent_info['seeding_time']) > 345600 and torrent_info['progress'] == 100 and float(torrent_info['ratio']) > 1.1:
            TORRENTSREMOVED+=1
            TORRENTSPASSEDSEEDINGCONDITIONS+=1
            logger.debug('Remove - Torrent: %s [%s] State: %s Progress: %s Seed Time: %s Label: %s Ratio: %s' % (torrent_id,torrent_info['name'],torrent_info['state'],torrent_info['progress'],torrent_info['seeding_time'],torrent_info['label'], torrent_info['ratio']))
            return 'D'
        if 'Unregistered torrent' in torrent_info['tracker_status']:
            TORRENTSREMOVED+=1
            TORRENTSREMOVED+=1
            logger.debug('Remove [Unregistered Torrent] - Torrent: %s [%s] State: %s Progress: %s Seed Time: %s Label: %s Ratio: %s Tracker Status: %s' % (torrent_id,torrent_info['name'],torrent_info['state'],torrent_info['progress'],torrent_info['seeding_time'],torrent_info['label'], torrent_info['ratio'], torrent_info['tracker_status']))
            return 'D'
    return ''

logger.info('Start Processing Deluge')
filter_torrents({},['tracker','seeding_time', 'name', 'state', 'progress','label', 'ratio', 'tracker_status'],torrentAction)
logger.info('Total AutoDL  Torrents: %i' % (TORRENTSLABLEDCOUNT))
logger.info('Total AutoDL  Torrents to be Removed: %i - [Unregistered: %i] [Completed: %i]' % (TORRENTSREMOVED, TORRENTSREMOVED, TORRENTSPASSEDSEEDINGCONDITIONS))
logger.info('Finished Run')
