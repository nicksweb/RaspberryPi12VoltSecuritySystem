#import functions

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

# globals.py for monitor.py and PiAlarmSystem
# Define necessary globals here as needed...

# AlarmSet
# Set how many times alarm will take a positive reading before Setting off the AlarmSet
MinAlarmTriggers = 4 # Set a threshold before alarm will sound
CurrentTriggers = [0,0,0,0] # Always starts at 0 and resets to 0 when system is not armed.
#Status_Armed = 0 # Changes to 1 if an Alarm is armed. MAY need to change this to an array - To reduce Database Calls.
arrayStatusArmed = [0,0,0,0]
AlarmAudible = 1 # Intial Value for Screamer is 1 (Can be set from Database and variable is overridden)
AlarmTime = 30 # 300 seconds is the maximun time for an Australian Alarm.
AlarmLoop = 10 # How many times should the alarm loop before switching off - 10 Times is 1 Hour approx.
AlarmCalled = 0 # Default to 0 as it ensures alarm loop isn't recalled (Calling an endless number of threads).
AlarmTempMute = 0
AlarmClear=0
AlarmDelay=20

reedSwitches=[2,3]

ZoneinAlarm=99  # 99 is used as an initialization value and the fact there's no 99 sensor.
run_once=0

# Global Threads
thread_list = [] # Used for Threading.
