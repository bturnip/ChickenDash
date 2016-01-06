# -*- coding: utf-8 -*-
"""
Danny Anderson
20151017

packet sniffing code started here:
https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8

# sms messaging code from Alex Le
# https://gist.github.com/alexle/1294495

@author: bturnip
"""

import cdd_meta as meta
import sys
import csv
import datetime
from datetime import date
from astral import Astral
import os
from scapy.all import *
import argparse
import smtplib


# =========================================================================
# Argument parsing
# =========================================================================
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--force_listen"\
                    ,help = "Force the packet sniffer (override the time settings.)"\
                    , action = "store_true")
parser.add_argument("-s", "--show_log"
                    ,help = "display log at end of run"
                    ,action="store_true")
parser.add_argument("-k", "--kill_sms"
                    ,help = "prevent SMS/MMS message from being sent"
                    ,action="store_true")

args = parser.parse_args()


# =========================================================================
# Variables
# =========================================================================
FILE = meta.CDD_DATA_FILE
LOG_FILE = meta.CDD_DIR + "/data/cdd_log_" + meta.YYYYMMDD + ".log"
CURRENT_TIME = meta.TIMEZONE.localize(datetime.datetime.now())

if args.kill_sms:
    MESSAGE_ENABLED = False
else:
    MESSAGE_ENABLED = True





# =========================================================================
# Prep logging
# =========================================================================
with open(LOG_FILE, 'w') as LOG:
    meta.WRITE_LOG(LOG_FILE, meta.full_name + " starting", True)

if args.force_listen:
    meta.WRITE_LOG(LOG_FILE, "--force_listen specified", True)
if args.show_log:
    meta.WRITE_LOG(LOG_FILE, "--show_log specified", True)
if args.kill_sms:
    meta.WRITE_LOG(LOG_FILE, "---kill_sms specified", True)


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
               'Calculating sunset and dusk for city: [' + city_name + ']')
meta.WRITE_LOG(LOG_FILE,
               'Astral calculation for Sunset: ' + str(sun['sunset']), True)
meta.WRITE_LOG(LOG_FILE,
               'Astral calculation for Dusk:   ' + str(sun['dusk']), True)
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
if(CURRENT_TIME > DUSK_TIME and not args.force_listen):
    meta.WRITE_LOG(LOG_FILE,
                   'Current time is past dusk, skipping execution'
                   , True)
    MESSAGE_ENABLED = False
else:
    while(not meta.IS_DASH_BUTTON_01_PUSHED
          and (CURRENT_TIME < DUSK_TIME or args.force_listen)):

        i += 1
        if (i > 25 and args.force_listen):
            print "force_list option exceeded 25 loops, exiting loop"
            break

        print sniff(prn=meta.arp_display, filter="arp", store=0, count=meta.NUM_SNIFFS)
        CURRENT_TIME = meta.TIMEZONE.localize(datetime.datetime.now())
        print "sniff run [" + str(i), "]", CURRENT_TIME, "BUTTON_PUSHED_STATE: ", meta.IS_DASH_BUTTON_01_PUSHED

    print "LOOP EXIT", "Button Push:", meta.IS_DASH_BUTTON_01_PUSHED, CURRENT_TIME


if meta.IS_DASH_BUTTON_01_PUSHED:
    meta.WRITE_LOG(LOG_FILE,'Button pushed, program exit...')
else:
    meta.WRITE_LOG(LOG_FILE,'Button not pushed, sending SMS warning')
    if MESSAGE_ENABLED:
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        server.login( meta.GMAIL_ADDRESS, meta.APP_PASS )

        # Send text message through SMS gateway of destination number
        SMS_MESSAGE = 'ChickenDash button warning!  Check roost door.  ' \
                    + meta.today.strftime('%a %b %d')
        # print "+++DEBUG: SMS_MESSAGE = [" + SMS_MESSAGE + "]"
        server.sendmail('ChickenDash'
                        , meta.DESTINATION_NUMBER
                        , SMS_MESSAGE)
    else:
        meta.WRITE_LOG(LOG_FILE,"MESSAGE_ENABLED is False, skipping SMS")


# =========================================================================
# Exit
# =========================================================================
if args.show_log:
    meta.SHOW_LOG(LOG_FILE)

