#import functions
from OpenSSL import SSL
from array import array
#from functions import *

# SQL Database Information
dbUser='pmatest'
dbPassword='dummypassword'
dbHost='127.0.0.1'
dbDatabase='piSecuritySystem'

# These details are here and are replaced with data from the Database
# Please note Email and Server details must be provided in the Settings Database.
smtpEmail="genericemail@gmail.com"
smtpUser="genericemail@gmail.com"
smtpPassword="fakepassword" # Get an App Password.
smtpServer="smtp.gmail.com"
smtpPort=465
mailRecip=('emailrecip@test.com','emailrecip2@test.com')
# Set the Type such as TLS / SSL in sendmail.py

# Globals for Key Fobs 
keyAList = [0,1,2,3]
# keyB is automatically used as the off key for A zones. 
keyBList = [0,1] # Selected Zone only 
keyCList = [3] # Unassigned...                  #Use 99 for an unsigned key. 

keyA=0
keyB=0
keyC=0

# globals.py for monitor.py and PiAlarmSystem
# Define necessary globals here as needed...

# AlarmSet
# Set how many times alarm will take a positive reading before Setting off the AlarmSet
MinAlarmTriggers = 4 # Set a threshold before alarm will sound
CurrentTriggers = [0,0,0,0] # Always starts at 0 and resets to 0 when system is not armed.
#Status_Armed = 0 # Changes to 1 if an Alarm is armed. MAY need to change this to an array - To reduce Database Calls.
arrayStatusArmed = [0,0,0,0]
AlarmAudible = 0 # Intial Value for Screamer is 1 (Can be set from Database and variable is overridden)
AlarmTime = 30 # 300 seconds is the maximun time for an Australian Alarm.
AlarmLoop = 20 # How many times should the alarm loop before switching off - 10 Times is 1 Hour approx.
AlarmCalled = 0 # Default to 0 as it ensures alarm loop isn't recalled (Calling an endless number of threads).
AlarmTempMute = 0
AlarmClear=0 # A virtual switch that turns the alarms off
AlarmDelay=20  # Delaying the time you have to get out before the alarm detects threats - Also the Grace period for switching off the alarm.
Alarm_Delay=0 # Add on increments for each time the remote is pressed.

reedSwitches=[2,3]

ZoneinAlarm=99  # 99 is used as an initialization value and the fact there's no 99 sensor.
run_once=0
alarm_delay=0 # Used for preventing sensors from triggering alarm during grace period.

Arming_Delay=0 # Used a boolean
ArmingDelay=20
ArmingDelayRunning=0 # Used by functions for counting.
delayArmingx=0
runOnce_AlarmDelay=0

# Used for Emergency Alarm (Instant ALarm)
EmergencyActivated=0

# Display Zone information to the screen.
loggingEnabled=1

# Global Threads
thread_list = [] # Used for Threading.


import os
context=SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join(os.path.dirname(__file__),'piss.crt') 
key = os.path.join(os.path.dirname(__file__),'piss.key')

