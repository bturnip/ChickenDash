# -*- coding: utf-8 -*-
"""
Danny Anderson
20151017

@author: bturnip
"""
import datetime
import os
import pytz
from scapy.all import *

# =========================================================================
# Variables
# =========================================================================
DEBUG_FLAG = True
today = datetime.datetime.today()
YYYYMMDD = today.strftime('%Y%m%d%H%M%S')
CITY = "Little Rock"
# Kludge, though this comes out automatically
# using Astral if the city is recognized
TIMEZONE = pytz.timezone('US/Central')


# =========================================================================
# Button Variables
# =========================================================================
DASH_BTTN_MAC_01 = '74:75:48:24:39:fd'
DASH_BTTN_MAC_02 = ''


NUM_SNIFFS = 10
IS_DASH_BUTTON_01_PUSHED = False


# =========================================================================
# Location
# =========================================================================
pass


# =========================================================================
# File paths
# =========================================================================
CDD_DIR = "/home/bturnip/Documents/Code/python/ChickenDash"
CDD_DATA_FILE = CDD_DIR + "data/cdd.csv"


# =========================================================================
# Needlessly complicated versioning
# =========================================================================
version = '0.1'

v = int(version[0])

avatar_dict = {
    4:"Perching Penny"
    ,3:"Sassy Sally"
    ,2:"Irresistible Imogene"
    ,1:"Nesting Nugget"
    ,0:"Roaming Road Runner"}

avatar = avatar_dict[v]


# =========================================================================
# For DEBUG
# =========================================================================
#print "+++DEBUG:", "DASH_BTTN_MAC",DASH_BTTN_MAC
#print "+++DEBUG:", "avatar",avatar
#print "+++DEBUG:", "version",version
#print "+++DEBUG:", "CDD_DIR",CDD_DIR
#print "+++DEBUG:", "CDD_DATA",CDD_DATA
#print "+++DEBUG:", "CDD_DATA_FILE",CDD_DATA_FILE


# =========================================================================
# Logging function
# =========================================================================
def WRITE_LOG(file, message, print_option = False):
    lognow = datetime.datetime.today()
    logdate = lognow.strftime('%c')

    # strip one or more newlines (we'll add one later ourselves)
    while (message[-1] == "\n"):
        message = message[:-1]

    log_message = logdate + "|" + message + "\n"

    if os.path.isfile(file):
        with open(file, "a") as f:
            f.write(log_message)
    else:
        print "+++ERROR", "WRITE_LOG(file, message):", file, message, " failed!"

    if print_option:
        print log_message.rstrip(os.linesep)


# =========================================================================
# Calculate time diffs
# =========================================================================
def SECONDS_BETWEEN(event_time, print_option = False):

    RIGHT_NOW = TIMEZONE.localize(datetime.datetime.now())

    # we passed in a date, right?
    if isinstance(event_time, datetime.datetime):
        if (event_time >= RIGHT_NOW):
            if print_option:
                print "+++INFO: SECONDS_BETWEEN(): future event"
                print (event_time - RIGHT_NOW).total_seconds()
            return int((event_time - RIGHT_NOW).total_seconds())
        else:
            if print_option:
                print "+++INFO: SECONDS_BETWEEN(): past event"
                print (RIGHT_NOW - event_time).total_seconds()
            return int((RIGHT_NOW - event_time).total_seconds())
    else:
        print "+++ERROR: YOU ARE KILLING ME, SMALLS!!"


# =========================================================================
def arp_display(pkt):
# =========================================================================
    global IS_DASH_BUTTON_01_PUSHED

    try:
        if pkt[ARP].op == 1:
            if pkt[ARP].psrc == '0.0.0.0':
                if pkt[ARP].hwsrc == DASH_BTTN_MAC_01:
                    print "Pushed Dash Button"
                    IS_DASH_BUTTON_01_PUSHED = True
                else:
                    print "ARP Probe from unknown device: " + pkt[ARP].hwsrc
            else:
                pass

    except IndexError as e:
        print e

