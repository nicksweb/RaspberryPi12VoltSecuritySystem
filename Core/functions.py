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

def delayArming(): # Used for delaying a zone from detecting movement until specified.
    x = 0

    if(globals.Arming_Delay == 1 and globals.AlarmCalled==0):

        if globals.ArmingDelayRunning+globals.ArmingDelay < 60:
            globals.ArmingDelayRunning+=globals.ArmingDelay
        else:
            globals.ArmingDelayRunning=(60-globals.ArmingDelay)


    if(globals.Arming_Delay == 0 and x < globals.ArmingDelay+globals.ArmingDelayRunning and globals.AlarmCalled==0):
        globals.Arming_Delay=1 # Prevent threads from being ran.

        log(str('Delaying Arming for approx:\t%d\t' % (globals.ArmingDelayRunning+globals.ArmingDelay)))

        while ( x < globals.ArmingDelayRunning+globals.ArmingDelay):
            time.sleep(1)
            log(str('Delaying Arming for approx:\t%d\t<\t%d\t' % (x, globals.ArmingDelayRunning+globals.ArmingDelay)))
            x += 1
            if x == globals.ArmingDelayRunning+globals.ArmingDelay:
                globals.Arming_Delay=0
                globals.ArmingDelayRunning=0
                globals.AlarmCalled = 0


def timerBeeper(timerDecimal):
        switcher={
            0: Decimal(0.5),
            1: Decimal(0.2)
        }
        return switcher.get(timerDecimal,"Invalid result fetches")

def beeper(w,x,timeChoice): # Number of times to beep
    # Do something
    timeVal = float(timerBeeper(timeChoice))

    log(str('\nBeeping:\t%d\t\n' % (x)))

    if(w == 0):     # Change timeVal to 0.5 so that when alarm is disabling it's a long beep.
        timeVal = float(0.5)
        # Short beeps remain the same at 0.2 (As per timerBeeper function above).
        w = 1 # Set w to 1 so output pin will be high (On)

    for i in range(x):
        time.sleep(timeVal)
        pifacedigital.output_pins[0].value = w
        pifacedigital.output_pins[2].value = w
        time.sleep(timeVal)
        pifacedigital.output_pins[0].value = 0
        pifacedigital.output_pins[2].value = 0



def logAlarming(pin, status): # Logs the time an alarm is armed to the Database
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    sql = "INSERT INTO piSS_Log_Arming (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)
    cnx.commit()
    cnx.close()

    #returnedStatus = getLastSensorLog(globals.ZoneinAlarm)
    zoneinfo = PISSZoneStatus(pin)
    log(str('\nZone Set:\t%s\n' % (zoneinfo[2])))

def pirSensorLog(pin, status):
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)
    cnx.commit()
    cnx.close()

    #returnedStatus = getLastSensorLog(globals.ZoneinAlarm)
    zoneinfo = PISSZoneStatus(pin)
    log(str('\nMotion:\t%s\t\t%d \n' % (zoneinfo[2],status)))


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

    if(databaseValue==0): #
        aa = threading.Thread(target=delayArming)
        globals.thread_list.append(aa)
        aa.start()

    RemoteUpdateSetZones(zone, DatabasePullStatus(databaseValue))
    beeper(DatabasePullStatus(databaseValue), 4, DatabasePullStatus(databaseValue))
    logAlarming(9999, DatabasePullStatus(databaseValue))

def RemoteInput5(event): # C Key on Remote
    zone = 2
    returnedStatus = remoteSensorLogSelect(zone)
    databaseValue = returnedStatus[3]

    if(globals.arrayStatusArmed[zone]==0): #
        aa = threading.Thread(target=delayArming)
        globals.thread_list.append(aa)
        aa.start()


    RemoteUpdateSingleZone(zone, DatabasePullStatus(databaseValue))
    beeper(DatabasePullStatus(databaseValue), 3, DatabasePullStatus(databaseValue))
    logAlarming(2, DatabasePullStatus(databaseValue))
    globals.arrayStatusArmed[zone] = DatabasePullStatus(databaseValue)


def RemoteInput6(event): # Button B on remote.
    zone = 1
    returnedStatus = remoteSensorLogSelect(zone)
    databaseValue = returnedStatus[3]

    if(globals.arrayStatusArmed[zone]==0): #
        aa = threading.Thread(target=delayArming)
        globals.thread_list.append(aa)
        aa.start()

    RemoteUpdateSingleZone(zone, DatabasePullStatus(databaseValue))
    beeper(DatabasePullStatus(databaseValue), 2, DatabasePullStatus(databaseValue))
    logAlarming(1, DatabasePullStatus(databaseValue))
    globals.arrayStatusArmed[zone] = DatabasePullStatus(databaseValue)

def RemoteInput7(event): # Button A on remote.
    zone = 0
    returnedStatus = remoteSensorLogSelect(zone)
    databaseValue = returnedStatus[3]

    if(globals.arrayStatusArmed[zone]==0): #
        aa = threading.Thread(target=delayArming)
        globals.thread_list.append(aa)
        aa.start()

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

   zoneinfo = PISSZoneStatus(zone)

   if globals.arrayStatusArmed[zone] == 1 and globals.alarm_delay == 0: #or globals.arrayStatusArmed[9999] == 0:
      globals.CurrentTriggers[zone] += 1

      if zone in globals.reedSwitches:
          globals.CurrentTriggers[zone] >= globals.MinAlarmTriggers+1 # So it trips the alarm instantly - It's a Reed Switch.

      print("Current Trigers 1:",globals.CurrentTriggers[zone])

      log(str('\n%s Zone has triggered a checkZone()\n' % (zoneinfo[2])))

   # Could use global.ClearAlarm as a variable to switch a triggered alarm off and set CurrentTriggers to 0 (Restarting the detection process).
   if globals.arrayStatusArmed[zone] == 0 and globals.AlarmCalled == 0 and globals.run_once == 0:
      globals.CurrentTriggers[zone] = 0

   if globals.CurrentTriggers[zone] >= globals.MinAlarmTriggers and globals.AlarmCalled == 0 and globals.Arming_Delay == 0:
      log(str('\n%s Zone has triggered %s activation of the Zone\'s sensor' % (str(zoneinfo[2]),str(globals.CurrentTriggers[zone]))))
      log('\n\tAlarm Thread Starting.\n')
      aa = threading.Thread(target=ActivateAlarm, args=(zone,))

      globals.CurrentTriggers[zone] = 0
      globals.ZoneinAlarm=zone

      globals.thread_list.append(aa)
      aa.start()

      # initZones()  Use only for testing - Used to set Database values back to 0 for Alarm's Activation Status - If using in producti on - Once alarm is activated
      #             It will not reactivate after it's first activation.

def Screamer():

    time.sleep(2) # Short delay to let ScreamerControl Catch-up for AlarmDelay if used...

    while (globals.AlarmCalled == 1):  # Removed globals.AlarmAudible (globals.AlarmAudible==1 and )

        while (globals.Alarm_Delay==1): # and globals.AlarmCalled == 1):
            print("Screamer Waiting")
            time.sleep(1)

        while (globals.AlarmTempMute == 0 and globals.AlarmCalled == 1 and globals.Alarm_Delay==0):
            # Screamer is 1.
            pifacedigital.output_pins[1].value = globals.AlarmAudible # This would usually be one when not being tested.
            log("\n\n\t\tSCREAMER IS ON!!!!!\n\n")
            # Output pin 3 is strobe on the flashing siren.
            pifacedigital.output_pins[3].value = 1
            # Output pin 2 is the solid light on the siren.
            pifacedigital.output_pins[2].value = 0
            #print("Alarm is sounding")
            time.sleep(1)

        while (globals.AlarmTempMute == 1 and globals.AlarmCalled == 1 and globals.Alarm_Delay==0):
            # Mutes the Alarm if sounding for longer than AlarmTime (Refer to ScreamerControl)
            log("\n\n\t\tSCREAMER IS Muted!!!!!\n\n")
            pifacedigital.output_pins[1].value = 0
            pifacedigital.output_pins[3].value = 0
            pifacedigital.output_pins[2].value = 1
            #print("Alarm is muted")
            time.sleep(1)

        log("ALarm Temp Mute: %d" % (globals.AlarmTempMute))
        log("ALarm Called: %d" % (globals.AlarmCalled))
        log("ALarm Called: %d" % (globals.Alarm_Delay))

    # Set Screamer to off just in case.
    pifacedigital.output_pins[1].value = 0
    pifacedigital.output_pins[2].value = 0
    pifacedigital.output_pins[3].value = 0

def ScreamerOff():
    pifacedigital.output_pins[1].value = 0
    pifacedigital.output_pins[2].value = 0 # Solid light
    pifacedigital.output_pins[3].value = 0 # Flashing Strobe Effect
    # Screamer is now off.
    print("Alarm is off now...")

def ScreamerControl():

    x = 0

    log("Screamer Control %d %d %d " % (globals.AlarmDelay, globals.AlarmClear, globals.Alarm_Delay))

    while(globals.AlarmDelay > x and globals.AlarmClear==0 and globals.Alarm_Delay==1 and globals.AlarmCalled == 1): # and globals.arrayStatusArmed[globals.ZoneinAlarm] == 1

        log("Delaying Alarm:\t%d" % (globals.AlarmDelay-x))


        #Start Beeper in separate thread so it does't slow this thread down.
        if (x == 0): # Only start the thread once.
            ad = threading.Thread(target=beeper, args=(1,globals.AlarmDelay-1,0))
            ad.start()

        x += 1

        if globals.AlarmDelay == x:
            x = 0
            globals.AlarmTempMute = 0
            globals.Alarm_Delay = 0
            log("Alarm_Delay finshed")

        time.sleep(1)

    x = 0
    w = 0
    count = 0

    while (globals.AlarmCalled == 1 and globals.AlarmLoop >= x):
        while (globals.AlarmTempMute == 0 and globals.AlarmCalled == 1 and globals.AlarmTime > count):
            log("Alarm is Sounding... Sleeping Alarm for, %d seconds." % (globals.AlarmTime-count))
            count += 1
            time.sleep(1)

            if (globals.AlarmTime == count):
                globals.AlarmTempMute = 1 # Switch to Once
                count = 0


        while (globals.AlarmTempMute == 1 and globals.AlarmTime > count and globals.AlarmCalled == 1):
            log("Alarm is Muted... Sleeping Alarm for, %d seconds." % (globals.AlarmTime-count))
            count += 1
            time.sleep(1)

            if (globals.AlarmTime == count):
                globals.AlarmTempMute = 0 # Switch to Once
                count = 0

        x += 1

        log("ALarm Loops Remaining: %d" % (globals.AlarmLoop-x))
        log("ALarm Called: %d" % (globals.AlarmCalled))

        if ((globals.AlarmLoop-x)==0):
            globals.AlarmCalled = 0
            globals.AlarmTempMute = 0
            globals.run_once=0
            #globals.AlarmCalled = 0
            x = x + globals.AlarmLoop
            log("Alarm control has ended...")
            globals.CurrentTriggers = [0,0,0,0]
            #xxx

            break





def ActivateAlarm(name):
    # Initiate Class for Screamer...
    # Function is used so it can be cancelled easily.
    aaAlarm = threading.Thread(target=Screamer)
    aaAlarmControl = threading.Thread(target=ScreamerControl)

    returnedStatus = getLastSensorLog(globals.ZoneinAlarm)
    zoneinfo = PISSZoneStatus(globals.ZoneinAlarm)

    setConfigurationSettings('ZoneinAlarm',globals.ZoneinAlarm)

    aaEmailNotification = threading.Thread(target=sendNotification, args=("Urgent - Alarm Notifcation - " + str(returnedStatus[0]),"Zone " + str(zoneinfo[2]) + " is in Alarm","Bryony Crt","Time of Incident: " + str(returnedStatus[0]),"nicholas@suburbanau.com"))

    globals.AlarmCalled = 1

    print("At Activate Alarm")
    print(globals.AlarmCalled, " ", globals.run_once, " ", globals.AlarmClear, " ", globals.arrayStatusArmed[globals.ZoneinAlarm])

    while (globals.AlarmCalled==1): # Don't need this anymore sum(globals.arrayStatusArmed) > 0 and ...
       # Do something...
       print("Waiting at alarm clear")

       if globals.run_once == 0 and globals.AlarmClear == 0 and globals.arrayStatusArmed[globals.ZoneinAlarm] == 1:
          log("Starting Alarm Threads - ActivateAlarm (True) - Run_Once")
          globals.thread_list.append(aaAlarm)
          globals.thread_list.append(ScreamerControl)
          globals.thread_list.append(aaEmailNotification)
          # Check Database for Silence is enabled...
          returnedStatus = PISSZoneStatus(10001)
          databaseValue11x = returnedStatus[3]
          globals.AlarmAudible=databaseValue11x

          globals.Alarm_Delay=1
          aaAlarmControl.start()
          ## time.sleep(globals.AlarmDelay)
          aaAlarm.start()
          aaEmailNotification.start()

          globals.run_once = 1

       while globals.AlarmCalled!=0 or globals.AlarmClear!=1 or globals.arrayStatusArmed[globals.ZoneinAlarm] != 0:

           if (globals.AlarmCalled==0 or globals.AlarmClear==1 or globals.arrayStatusArmed[globals.ZoneinAlarm] == 0):
               #InfTimerScreamer.cancel()
               RemoteUpdateSingleZone(10003, 0) # Update AlarmClear in DB.
               globals.CurrentTriggers = [0,0,0,0]
               globals.AlarmTempMute = 0
               globals.AlarmCalled=0
               globals.run_once = 0
               globals.ZoneinAlarm = 99
               ScreamerOff()
               globals.Arming_Delay=0
               globals.Alarming_Delay=0
               globals.AlarmClear=0
               time.sleep(1)
               ScreamerOff()
               setConfigurationSettings('ZoneinAlarm',globals.ZoneinAlarm)
               log("\n\tAlarm should now be off...")
               # Set Screamer to off.
               break
               #time.sleep(1)

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

    returnedStatus = PISSZoneStatus(3)
    databaseValue3 = returnedStatus[3]
    globals.arrayStatusArmed[2]=databaseValue3

    returnedStatus = PISSZoneStatus(9999)
    databaseValue9x = returnedStatus[3]
    #globals.arrayStatusArmed[3]=databaseValue9x

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

    returnedStatus = PISSZoneStatus(10004)
    databaseValue14x = returnedStatus[3]
    globals.AlarmDelay=databaseValue14x

    returnedStatus = PISSZoneStatus(10005)
    databaseValue15x = returnedStatus[3]
    globals.AlarmLoop=databaseValue15x

    returnedStatus = PISSZoneStatus(10006)
    databaseValue16x = returnedStatus[3]
    globals.ArmingDelay=databaseValue16x

    #log("Globals Updated")

def getConfigurationSettings(key): #Only ran once at program start-up and then every 30 minutes.
    sql = "select Value from piSS_Settings Where SettingKey = '%s';" % (key)
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchone()
    cnx.close()
    return result

def setConfigurationSettings(key,value):
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    sql = "Update piSS_Settings Set Value=%s Where SettingKey=%s;"
    val = (value, key)
    mycursor.execute(sql, val)
    cnx.commit()
    cnx.close()

    #zoneinfo = PISSZoneStatus(pin)
    #log(str('\nZone Set:\t%s\n' % (zoneinfo[2])))

def getLastSensorLog(zone): #Only ran once at program start-up and then every 30 minutes.
    sql = "Select * from piSS_SensorLog Where Port=%d Order By ID Desc Limit 1;" % (zone)
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchone()
    cnx.close()
    return result

def log(name):
    if globals.loggingEnabled:
        print(name)


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