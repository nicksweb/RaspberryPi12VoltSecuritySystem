# functions.py
import globals

# extras
import mysql.connector
import pifacedigitalio
import time
import mysql.connector
import threading

from decimal import *
from threading import Timer

# Function Variables...
cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
#listener = pifacedigitalio.InputEventListener(chip=pifacedigital)

# Global Variables for PiFaceDigitalIO
# Used for Interacting/Interfacing
pifacedigital = pifacedigitalio.PiFaceDigital()
listener = pifacedigitalio.InputEventListener(chip=pifacedigital)

#
# Global Functions
#
def logToScreen(message):
   print(message)
   print(globals.current_value)

#
# MySQL Functions
#


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
            0: Decimal(1),
            1: Decimal(0.2)
        }
        return switcher.get(timerDecimal,"Invalid result fetches")

def beeper(w,x,timeChoice): # Number of times to beep
        # Do something
        timeVal = float(timerBeeper(timeChoice))

        for i in range(x):
            time.sleep(timeVal)
            pifacedigital.output_pins[0].value = w
            # 1 is the Screamer...
            print("Should be beeping")
            time.sleep(timeVal)
            pifacedigital.output_pins[0].value = 0

def logAlarming(pin, status): # Logs the time an alarm is armed to the Database
    mycursor = cnx.cursor()

    sql = "INSERT INTO piSS_Log_Arming (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)
    cnx.commit()

def pirSensorLog(pin, status):
    mycursor = cnx.cursor()
    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"

    val = (str(pin), str(status))

    mycursor.execute(sql, val)
    cnx.commit()
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
    mycursor = cnx.cursor()
    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"

    val = (str(pin), str(status))

    mycursor.execute(sql, val)
    cnx.commit()
    print('Sensor', pin, 'is ', status, "record inserted.")
    print("Finished insertion")

def PISSZoneStatus(zone):
    sql = "select * from piSS_Zones Where Zone = %d;" % (zone)
    mycursor = cnx.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchone()
    return result

def remoteSensorLogSelect(zone):
    sql = "select * from piSS_Zones Where Zone = %d;" % (zone)

    mycursor = cnx.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchone()
    return result

def RemoteUpdateSetZones(zone, status):
    mycursor = cnx.cursor()
    sql = "Update piSS_Zones Set Status = %d WHERE Zone BETWEEN 0 AND %d;" % (status, zone)
    mycursor.execute(sql)
    cnx.commit()

def RemoteUpdateSingleZone(zone, status):
    mycursor = cnx.cursor()
    sql = "Update piSS_Zones Set Status = %d WHERE Zone = %d;" % (status, zone)
    mycursor.execute(sql)
    cnx.commit()

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
  RemoteUpdateSingleZone(2, 1)
  RemoteUpdateSingleZone(9999, 0)

# This zone checks if alarm should be activated and subsequently sounded.
def checkZone(zone):
   # Check if zone is armed in Global Variable - It's in the Database Already - But it's quicker to access a
   # local variable.

   print("ZONE", zone)

   if globals.arrayStatusArmed[zone] == 1:
      globals.CurrentTriggers += 1

   if sum(globals.arrayStatusArmed) == 0:
      globals.CurrentTriggers = 0
      print("Sum of sensors is 0")

   print(globals.CurrentTriggers)

   if globals.CurrentTriggers >= globals.MinAlarmTriggers:
      aa = threading.Thread(target=ActivateAlarm, args=(1,))
      print("Starting Alarm Thread")
      globals.thread_list.append(aa)
      aa.start()

      # Cleaning up
      globals.CurrentTriggers = 0
      initZones()

def ActivateAlarm(name):
    # Check Database for Silence is enabled...
    returnedStatus = PISSZoneStatus(10001)
    databaseValue11x = returnedStatus[3]
    globals.AlarmAudible=databaseValue11x

    # Initiate Class for Screamer...
    InfTimerScreamer = InfiniteTimer(15, Screamer)

    if (globals.AlarmAudible==1):
        InfTimerScreamer.start()
        #Carry out action...
        print("Thread %s: starting", name)
        time.sleep(2)
        beeper(1, 2, 1)
        print("Thread %s: finishing", name)



    # Set Screamer to on.

    # Send an email / SMS to the user / Whatapp / Singal Whatever is avaiable API wise.
    # Set of Screamer... for 5 mins...
    # ... if (globals.AlarmAudible)


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

    print("Globals Updated")

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