# functions.py
import globals
import alerts

# extras
import mysql.connector
import pifacedigitalio
import time
import mysql.connector
import threading

from decimal import *
from threading import Timer

# From Github (https://github.com/dimaba/sendmail)
#from sendmail import MailSender
from alerts import *

# Global Variables for PiFaceDigitalIO
# Used for Interacting/Interfacing
pifacedigital = pifacedigitalio.PiFaceDigital()
listener = pifacedigitalio.InputEventListener(chip=pifacedigital)

#
# PiFaceDigitalIO Functions
#
#Define required functions...
def DatabasePullStatus(i):
    switcher={
        0: 1,
        1: 0
    }
    return switcher.get(float(i),"Invalid result fetched")

def timerBeeper(timerDecimal):
        switcher={
            0: Decimal(0.5),
            1: Decimal(0.2)
        }
        return switcher.get(timerDecimal,"Invalid result fetches")

def beeper(w,x,timeChoice): # Number of times to beep
    # Do something
    timeVal = float(timerBeeper(timeChoice))
    
    if(w == 0):     # Change timeVal to 0.5 so that when alarm is disabling it's a long beep. 
        timeVal = float(0.5)
        # Short beeps remain the same at 0.2 (As per timerBeeper function above). 
        w = 1 # Set w to 1 so output pin will be high (On)

    for i in range(x):
        time.sleep(timeVal)
        pifacedigital.output_pins[0].value = w
        # 1 is the Screamer...
        print("Beeping: ", x, " Time: ", timeVal)
        time.sleep(timeVal)
        pifacedigital.output_pins[0].value = 0

def logAlarming(pin, status): # Logs the time an alarm is armed to the Database
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    sql = "INSERT INTO piSS_Log_Arming (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)
    cnx.commit()
    cnx.close()

def pirSensorLog(pin, status):
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)
    cnx.commit()
    cnx.close()
    print('Sensor', pin, 'is ', status, "record inserted.")
    print("Finished insertion")

def pirEventCall0(event):
    pin = 0
    status = pifacedigital.input_pins[pin].value
    pirSensorLog(pin, status)
    checkZone(pin)

def pirEventCall1(event):
    pin = 1
    status = pifacedigital.input_pins[pin].value
    pirSensorLog(pin, status)
    checkZone(pin)

def pirEventCall2(event):
    pin = 2
    status = pifacedigital.input_pins[pin].value
    pirSensorLog(pin, status)
    checkZone(pin)

def pirEventCall3(event):
    pin = 3
    status = pifacedigital.input_pins[pin].value
    pirSensorLog(pin, status)
    checkZone(pin)

def remoteSensorLog(pin, status):
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)
    cnx.commit()
    cnx.close()
    print('Sensor', pin, 'is ', status, "record inserted.")
    print("Finished insertion")

def PISSZoneStatus(zone):
    sql = "select * from piSS_Zones Where Zone = %d;" % (zone)
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchone()
    cnx.close()
    return result

def remoteSensorLogSelect(zone):
    sql = "select * from piSS_Zones Where Zone = %d;" % (zone)
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchone()
    cnx.close()
    return result

def RemoteUpdateSetZones(zone, status):
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    sql = "Update piSS_Zones Set Status = %d WHERE Zone BETWEEN 0 AND %d;" % (status, zone)
    mycursor.execute(sql)
    cnx.commit()
    cnx.close()

def RemoteUpdateSingleZone(zone, status):
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    sql = "Update piSS_Zones Set Status = %d WHERE Zone = %d;" % (status, zone)
    mycursor.execute(sql)
    cnx.commit()
    cnx.close()

def RemoteInput4(event): # D Key on Remote
    zone = 9999
    returnedStatus = remoteSensorLogSelect(zone)
    databaseValue = returnedStatus[3]
    RemoteUpdateSetZones(zone, DatabasePullStatus(databaseValue))
    beeper(DatabasePullStatus(databaseValue), 4, DatabasePullStatus(databaseValue))
    logAlarming(9999, DatabasePullStatus(databaseValue))
    globals.arrayStatusArmed[3] = DatabasePullStatus(databaseValue)

def RemoteInput5(event): # C Key on Remote
    zone = 2
    returnedStatus = remoteSensorLogSelect(zone)
    databaseValue = returnedStatus[3]
    RemoteUpdateSingleZone(zone, DatabasePullStatus(databaseValue))
    beeper(DatabasePullStatus(databaseValue), 3, DatabasePullStatus(databaseValue))
    logAlarming(2, DatabasePullStatus(databaseValue))
    globals.arrayStatusArmed[zone] = DatabasePullStatus(databaseValue)

def RemoteInput6(event): # Button B on remote.
    zone = 1
    returnedStatus = remoteSensorLogSelect(zone)
    databaseValue = returnedStatus[3]
    RemoteUpdateSingleZone(zone, DatabasePullStatus(databaseValue))
    beeper(DatabasePullStatus(databaseValue), 2, DatabasePullStatus(databaseValue))
    logAlarming(1, DatabasePullStatus(databaseValue))
    globals.arrayStatusArmed[zone] = DatabasePullStatus(databaseValue)

def RemoteInput7(event): # Button A on remote.
    zone = 0
    returnedStatus = remoteSensorLogSelect(zone)
    databaseValue = returnedStatus[3]
    RemoteUpdateSingleZone(zone, DatabasePullStatus(databaseValue))
    beeper(DatabasePullStatus(databaseValue), 1, DatabasePullStatus(databaseValue))
    logAlarming(0, DatabasePullStatus(databaseValue))
    globals.arrayStatusArmed[zone] = DatabasePullStatus(databaseValue)

def initZones(): # Ran at program start-up to set all zones to off.
  RemoteUpdateSingleZone(0, 0)
  RemoteUpdateSingleZone(1, 0)
  RemoteUpdateSingleZone(2, 0)
  RemoteUpdateSingleZone(9999, 0)

# This zone checks if alarm should be activated and subsequently sounded.
def checkZone(zone):

   if globals.arrayStatusArmed[zone] == 1: #or globals.arrayStatusArmed[9999] == 0:
      globals.CurrentTriggers[zone] += 1

      if zone in globals.reedSwitches:
          globals.CurrentTriggers[zone] = globals.MinAlarmTriggers+1 # So it trips the alarm instantly - It's a Reed Switch.

      print("Current Trigers 1:",globals.CurrentTriggers[zone])

   # Could use global.ClearAlarm as a variable to switch a triggered alarm off and set CurrentTriggers to 0 (Restarting the detection process).
   if globals.arrayStatusArmed[zone] == 0 and globals.AlarmCalled == 0:
      globals.CurrentTriggers[zone] = 0
      print("Current Trigers :",globals.CurrentTriggers[zone])

   if globals.CurrentTriggers[zone] >= globals.MinAlarmTriggers and globals.AlarmCalled == 0:
      print("Alarm Triggers currently,", globals.CurrentTriggers[zone])
      aa = threading.Thread(target=ActivateAlarm, args=(zone,))

      #globals.CurrentTriggers[zone] = 0 # Set back to 0
      globals.CurrentTriggers[zone] = 0
      globals.ZoneinAlarm=zone

      print("Starting Alarm Thread")
      globals.thread_list.append(aa)
      aa.start()

      # initZones()  Use only for testing - Used to set Database values back to 0 for Alarm's Activation Status - If using in producti on - Once alarm is activated
      #             It will not reactivate after it's first activation.

def Screamer():
    
    time.sleep(2) # Short delay to let ScreamerControl Catch-up for AlarmDelay if used... 

    while (globals.AlarmAudible==1 and globals.AlarmCalled == 1):
        
        while (globals.AlarmTempMute == 0 and globals.AlarmCalled == 1):
            # Screamer is now on.
            pifacedigital.output_pins[2].value = 1
            #print("Alarm is sounding")
            time.sleep(1)

        while (globals.AlarmTempMute == 1 and globals.AlarmCalled == 1):
            # Mutes the Alarm if sounding for longer than AlarmTime (Refer to ScreamerControl)
            pifacedigital.output_pins[2].value = 0
            #print("Alarm is muted")
            time.sleep(1)

    # Set Screamer to off just in case.
    pifacedigital.output_pins[2].value = 0

def ScreamerOff():
    pifacedigital.output_pins[2].value = 0
    # Screamer is now off.
    print("Alarm is off now...")

def ScreamerControl():

    x = 0
    
    
    
    while(globals.AlarmDelay >= x):
        AlarmTempMute = 1
        time.sleep(1)
        print("Delaying Alarm")
        #Start Beeper in separate thread so it does't slow this thread down. 
        if (x == 0): # Only start the thread once. 
            ad = threading.Thread(target=beeper, args=(1,globals.AlarmDelay,0))
            ad.start()
        x += 1 
        
        if globals.AlarmDelay == x:
            x = 0
            AlarmTempMute = 0
            print("Delay finished")
            break
    
    x = 0

    while (globals.AlarmAudible==1 and globals.AlarmCalled == 1 and globals.AlarmLoop >= x):
        if (globals.AlarmTempMute == 0):
            print("Alarm is Sounding... Sleeping Alarm for, ", globals.AlarmTime, " seconds.")
            time.sleep(globals.AlarmTime)
            globals.AlarmTempMute = 1 # Switch to Once


        if (globals.AlarmTempMute == 1):
            print("Alarm is Muted... Muting Alarm for, ", globals.AlarmTime, " seconds.")
            time.sleep(globals.AlarmTime)
            globals.AlarmTempMute = 0

        if (globals.AlarmCalled == 0):
            globals.AlarmTempMute = 0
            print("Alarm control has ended...")
            break

        x += 1

def ActivateAlarm(name):
    # Initiate Class for Screamer...
    # Class is used so it can be cancelled easily.
    #InfTimerScreamer = InfiniteTimer(10, Screamer)
    aaAlarm = threading.Thread(target=Screamer)
    aaAlarmControl = threading.Thread(target=ScreamerControl)

    returnedStatus = getLastSensorLog(globals.ZoneinAlarm)
    zoneinfo = PISSZoneStatus(globals.ZoneinAlarm)
    #globals.arrayStatusArmed[0]=databaseValue0
    #def getLastSensorLog(zone): #Only ran once at program start-up and then every 30 minutes.

    #print(returnedStatus[0])
    #print(convertSQLDateTimeToTimestamp(returnedStatus[0]))

    aaEmailNotification = threading.Thread(target=sendNotification, args=("Urgent - Alarm Notifcation - " + str(returnedStatus[0]),"Zone " + str(zoneinfo[2]) + " is in Alarm","Bryony Crt","Time of Incident: " + str(returnedStatus[0]),"nicholas@suburbanau.com"))

    #if (globals.AlarmAudible==1 and globals.AlarmCalled==1):
        #Carry out action...
        #InfTimerScreamer.start()
    #    print("Starting Alarm Thread - ActivateAlarm (In If)")
    #   globals.thread_list.append(aaAlarm)
    #   globals.thread_list.append(ScreamerControl)
    #   globals.thread_list.append(aaEmailNotification)

        # Check Database for Silence is enabled...
    #   returnedStatus = PISSZoneStatus(10001)
    #   databaseValue11x = returnedStatus[3]
    #   globals.AlarmAudible=databaseValue11x

    #   print("Starting all the alarm Threads and sending an email.")
    #   aaAlarm.start()
    #   aaAlarmControl.start()

    #print("AlarmCalled = 1")
    #globals.AlarmCalled = 1

    #if (globals.AlarmAudible==0 and globals.AlarmCalled == 1):
        # In here for testing still...
        #time.sleep(10)
        # Send Email Thread (Function)

    while True: # Don't need this anymore sum(globals.arrayStatusArmed) > 0 and ...
       # Do something...
       #print("In the while loop")
       globals.AlarmCalled = 1
       print("Waiting at Alarm Clear")

       if globals.run_once == 0:
          print("Starting Alarm Thread - ActivateAlarm (In If)")
          globals.thread_list.append(aaAlarm)
          globals.thread_list.append(ScreamerControl)
          globals.thread_list.append(aaEmailNotification)
          # Check Database for Silence is enabled...
          returnedStatus = PISSZoneStatus(10001)
          databaseValue11x = returnedStatus[3]
          globals.AlarmAudible=databaseValue11x

          print("Starting all the alarm Threads and sending an email.")
          aaAlarmControl.start()
          time.sleep(globals.AlarmDelay)
          aaAlarm.start()
          aaEmailNotification.start()

          globals.run_once = 1

       if globals.AlarmClear==1 or globals.arrayStatusArmed[globals.ZoneinAlarm] == 0:
           #InfTimerScreamer.cancel()
           globals.AlarmCalled = 0
           RemoteUpdateSingleZone(10003, 0) # Update AlarmClear in DB.
           globals.CurrentTriggers = [0,0,0,0]
           globals.AlarmTempMute = 0
           globals.run_once = 0
           globals.ZoneinAlarm = 99
           ScreamerOff()
           print("Alarm should now be off")
           # Set Screamer to off.
           break

       time.sleep(1)

        # Send an email / SMS to the user / Whatapp / Singal Whatever is avaiable API wise.
        # Perhaps implement the DirectSMS API for messaging or similar.
        # Set of Screamer... for 5 mins...

def UpdateGlobals():
    # UpdateGlobals Class goes here... Function...
    returnedStatus = PISSZoneStatus(0)
    databaseValue0 = returnedStatus[3]
    globals.arrayStatusArmed[0]=databaseValue0

    returnedStatus = PISSZoneStatus(1)
    databaseValue1 = returnedStatus[3]
    globals.arrayStatusArmed[1]=databaseValue1

    returnedStatus = PISSZoneStatus(2)
    databaseValue2 = returnedStatus[3]
    globals.arrayStatusArmed[2]=databaseValue2

    returnedStatus = PISSZoneStatus(9999)
    databaseValue9x = returnedStatus[3]
    globals.arrayStatusArmed[3]=databaseValue9x

    returnedStatus = PISSZoneStatus(10000)
    databaseValue10x = returnedStatus[3]
    globals.MinAlarmTriggers=databaseValue10x

    returnedStatus = PISSZoneStatus(10001)
    databaseValue11x = returnedStatus[3]
    globals.AlarmAudible=databaseValue11x

    returnedStatus = PISSZoneStatus(10002)
    databaseValue12x = returnedStatus[3]
    globals.AlarmTime=databaseValue12x

    returnedStatus = PISSZoneStatus(10003)
    databaseValue13x = returnedStatus[3]
    globals.AlarmClear=databaseValue13x

    print("Globals Updated")

def getConfigurationSettings(key): #Only ran once at program start-up and then every 30 minutes.
    sql = "select Value from piSS_Settings Where SettingKey = '%s';" % (key)
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchone()
    cnx.close()
    return result

def getLastSensorLog(zone): #Only ran once at program start-up and then every 30 minutes.
    sql = "Select * from piSS_SensorLog Where Port=%d Order By ID Desc Limit 1;" % (zone)
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchone()
    cnx.close()
    return result

##
##
##
##
## InfiniteTimer Class
##
##
##
##

class InfiniteTimer():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue: # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")
