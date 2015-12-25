# -*- coding: utf-8 -*-
"""
Danny Anderson
20151017

packet sniffing code started here:
https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8

@author: bturnip
"""

import cdd_meta as meta
#import google_calendar_api as google
import csv
import datetime
from datetime import date
from astral import Astral
import os
from scapy.all import *


# =========================================================================
# Variables
# =========================================================================
FILE = meta.CDD_DATA_FILE
LOG_FILE = meta.CDD_DIR + "/data/cdd_log_" + meta.YYYYMMDD + ".log"
CURRENT_TIME = meta.TIMEZONE.localize(datetime.datetime.now())
DEBUG_FLAG = meta.DEBUG_FLAG


# =========================================================================
# Prep logging
# =========================================================================
with open(LOG_FILE, 'w') as LOG:
    meta.WRITE_LOG(LOG_FILE, "ChickenDoorDash starting", True)


# =========================================================================
# Astral Variables
# =========================================================================
city_name = meta.CITY
a = Astral()
a.solar_depression = 'civil'
city = a[city_name]
timezone = city.timezone
sun = city.sun(date=date.today(), local=True)

SECONDS_TIL_SUNSET = meta.SECONDS_BETWEEN(sun['sunset'])
SECONDS_TIL_DUSK = meta.SECONDS_BETWEEN(sun['dusk'])
DUSK_TIME = sun['dusk']


meta.WRITE_LOG(LOG_FILE,
               'Calculating sunset and dusk for city: [' +  city_name + ']')
meta.WRITE_LOG(LOG_FILE,
               'Astral calculation for Sunset: ' + str(sun['sunset']))
meta.WRITE_LOG(LOG_FILE,
               'Astral calculation for Dusk:   ' + str(sun['dusk']))
meta.WRITE_LOG(LOG_FILE,
               'SECONDS_TIL_SUNSET: [' + str(SECONDS_TIL_SUNSET) + ']')
meta.WRITE_LOG(LOG_FILE,
               'SECONDS_TIL_DUSK: [' + str(SECONDS_TIL_DUSK) + ']')





# =========================================================================
# Main loop
# =========================================================================
# Once program starts, go into a listening loop until the dash button
# has been pushed OR dusk has arrived
# =========================================================================
i = 0
if(DEBUG_FLAG):
    # if DEBUGGING, allow 25 pings, regardless of time
    while (not meta.IS_DASH_BUTTON_01_PUSHED and i < 25):
        i += 1
        print sniff(prn=meta.arp_display, filter="arp", store=0, count=meta.NUM_SNIFFS)

        print "sniff run #" + str(i), "CURRENT_TIME:", CURRENT_TIME, "IS_CDD_BUTTON_PUSHED", meta.IS_DASH_BUTTON_01_PUSHED

    print "LOOP EXIT", "Button Push:", meta.IS_DASH_BUTTON_01_PUSHED, \
    "CURRENT_TIME", CURRENT_TIME
else:
    while (not meta.IS_DASH_BUTTON_01_PUSHED and CURRENT_TIME < DUSK_TIME):
        i += 1
        print sniff(prn=meta.arp_display, filter="arp", store=0, count=meta.NUM_SNIFFS)

        CURRENT_TIME = meta.TIMEZONE.localize(datetime.datetime.now())
        print "sniff run #" + str(i), "CURRENT_TIME:", CURRENT_TIME, "IS_CDD_BUTTON_PUSHED", meta.IS_DASH_BUTTON_01_PUSHED

        print "LOOP EXIT", "Button Push:", meta.IS_DASH_BUTTON_01_PUSHED, \
        "CURRENT_TIME", CURRENT_TIME










#start at 5pm
#does log exist?
#    yes- append
#    no - create

#calcuate dusk print sniff(prn=arp_display, filter="arp", store=0, count=NUM_SNIFFS)time

#start checking for ping
#if ping:
    #record and quit
#if dusk and not ping
    #record and notify
    #wait 10 mins
    #record and notify
    #wait 10 mins
    #record and notify


#This program uses the sniff() callback (paramter prn). The store parameter is set to 0 so that the sniff() function will not store anything (as it would do otherwise) and thus can run forever. The filter parameter is used for better performances on high load : the filter is applied inside the kernel and Scapy will only see ARP traffic.

##! /usr/bin/env python
#from scapy.all import *

#def arp_monitor_callback(pkt):
    #if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        #return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")

#sniff(prn=arp_monitor_callback, filter="arp", store=0)







