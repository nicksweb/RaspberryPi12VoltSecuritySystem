# SQL Database Information
dbUser='pmatest'
dbPassword='dummypassword'
dbHost='127.0.0.1'
dbDatabase='piSecuritySystem'

# globals.py for monitor.py and PiAlarmSystem
# Define necessary globals here as needed...

# AlarmSet
# Set how many times alarm will take a positive reading before Setting off the AlarmSet
MinAlarmTriggers = 2 # Set a threshold before alarm will sound
Status_Armed = 0 # Changes to 1 if an Alarm is armed. MAY need to change this to an array - To reduce Database Calls.