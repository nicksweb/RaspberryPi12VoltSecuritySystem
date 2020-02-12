# functions.py
import globals

# extras
import mysql.connector
import pifacedigitalio
import time
import mysql.connector

from decimal import *

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

        print (timeVal)

        for i in range(x):
            time.sleep(timeVal)
            pifacedigital.output_pins[0].value = w
            time.sleep(timeVal)
            pifacedigital.output_pins[0].value = 0

def logAlarming(pin, status): # Logs the time an alarm is armed to the Database
    mycursor = cnx.cursor()

    sql = "INSERT INTO piSS_Log_Arming (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)
    cnx.commit()

def pirEventCall0(event):
    mycursor = cnx.cursor()

    pin = 0

    status = pifacedigital.input_pins[pin].value
    print(pin, 'is ', status, "record inserted.")

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()

    print("Finished insertion")

def pirEventCall1(event):
    mycursor = cnx.cursor()

    pin = 1

    status = pifacedigital.input_pins[pin].value
    print(pin, 'is ', status, "record inserted.")

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()

    print("Finished insertion")

def pirEventCall2(event):
    mycursor = cnx.cursor()

    pin = 2

    status = pifacedigital.input_pins[pin].value
    print(pin, 'is ', status, "record inserted.")

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()

    print("Finished insertion")

def pirEventCall3(event):
    mycursor = cnx.cursor()

    pin = 3

    status = pifacedigital.input_pins[pin].value
    print(pin, 'is ', status, "record inserted.")

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()

    print("Finished insertion")

def RemoteInput4(event): # D Key on Remote
    mycursor = cnx.cursor()

    sql_select_Query = "select * from piSS_Zones Where Zone = 9999;"
    mycursor.execute(sql_select_Query)
    ReturnedStatus = mycursor.fetchone()

    databaseValue = ReturnedStatus[3]

    print('Begenning, ', databaseValue)
    print('Switch, ', DatabasePullStatus(databaseValue))

    sql = "Update piSS_Zones Set Status = %d WHERE Zone BETWEEN 0 AND 9999;" % (DatabasePullStatus(databaseValue))
    mycursor.execute(sql)

    cnx.commit()
    beeper(DatabasePullStatus(databaseValue), 4, DatabasePullStatus(databaseValue))
    print("Finished insertion")

    logAlarming(9999, DatabasePullStatus(databaseValue))

def RemoteInput5(event): # C Key on Remote
    mycursor = cnx.cursor()

    sql_select_Query = "select * from piSS_Zones Where Zone = 2;"
    mycursor.execute(sql_select_Query)
    ReturnedStatus = mycursor.fetchone()
    databaseValue = ReturnedStatus[3]

    print('Begenning, ', databaseValue)
    print('Switch, ', DatabasePullStatus(databaseValue))

    sql = "Update piSS_Zones Set Status = %d WHERE Zone = 2" % (DatabasePullStatus(databaseValue))
    mycursor.execute(sql)

    cnx.commit()
    beeper(DatabasePullStatus(databaseValue), 3, DatabasePullStatus(databaseValue))
    print("Finished insertion")

    logAlarming(2, DatabasePullStatus(databaseValue))

def RemoteInput6(event): # Button B on remote.
    mycursor = cnx.cursor()

    sql_select_Query = "select * from piSS_Zones Where Zone = 1;"
    mycursor.execute(sql_select_Query)
    ReturnedStatus = mycursor.fetchone()
    databaseValue = ReturnedStatus[3]

    print('Begenning, ', databaseValue)
    print('Switch, ', DatabasePullStatus(databaseValue))

    sql = "Update piSS_Zones Set Status = %d WHERE Zone = 1" % (DatabasePullStatus(databaseValue))
    mycursor.execute(sql)

    cnx.commit()
    beeper(DatabasePullStatus(databaseValue), 2, DatabasePullStatus(databaseValue))
    print("Finished insertion")

    logAlarming(1, DatabasePullStatus(databaseValue))

def RemoteInput7(event):
    mycursor = cnx.cursor()
    sql_select_Query = "select * from piSS_Zones Where Zone = 0;"
    mycursor.execute(sql_select_Query)
    ReturnedStatus = mycursor.fetchone()
    databaseValue = ReturnedStatus[3]

    print('Begenning, ', databaseValue)
    print('Switch, ', DatabasePullStatus(databaseValue))

    sql = "Update piSS_Zones Set Status = %d WHERE Zone = 0" % (DatabasePullStatus(databaseValue))
    mycursor.execute(sql)

    cnx.commit()

    beeper(DatabasePullStatus(databaseValue), 1, DatabasePullStatus(databaseValue))
    print("Finished insertion")

    logAlarming(0, DatabasePullStatus(databaseValue))