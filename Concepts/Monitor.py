import time
import schedule
import pifacedigitalio
import mysql.connector
from decimal import *

#Database Details
dbUser='pmatest'
dbPassword='dummypassword'
dbHost='127.0.0.1'
dbDatabase='piSecuritySystem'

import schedule
import time

def job():
    print("I'm working...")

def pirEventCall0(event):
    mycursor = cnx.cursor()

    pin = 0

    status = pifacedigital.input_pins[pin].value
    #pifacedigital.output_pins[pin].value = status
    print(pin, 'is ', status, "record inserted.")

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()
    #pifacedigital.output_pins[pin].toggle()

    print("Finished insertion")

def pirEventCall1(event):
    mycursor = cnx.cursor()

    pin = 1

    status = pifacedigital.input_pins[pin].value
    #pifacedigital.output_pins[pin].value = status
    print(pin, 'is ', status, "record inserted.")

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()
    #pifacedigital.output_pins[pin].toggle()

    print("Finished insertion")

def pirEventCall2(event):
    mycursor = cnx.cursor()

    pin = 2

    status = pifacedigital.input_pins[pin].value
    #pifacedigital.output_pins[pin].value = status
    print(pin, 'is ', status, "record inserted.")

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()
    #pifacedigital.output_pins[pin].toggle()

    print("Finished insertion")

def pirEventCall3(event):
    mycursor = cnx.cursor()

    pin = 3

    status = pifacedigital.input_pins[pin].value
    #pifacedigital.output_pins[pin].value = status
    print(pin, 'is ', status, "record inserted.")

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()
    #pifacedigital.output_pins[pin].toggle()

    print("Finished insertion")

class DatabaseCon:

    def connect(self):
        RemoteInput = mysql.connector.connect(user=dbUser,password=dbPassword,host=dbHost,database=dbDatabase)
        print("Database connected")

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

def monitorZones(): # Monitor Zones in SQL Database
    # Do what's required...
    print("Quering Database")

def ifAlarmActive(event): # IfAlarmActive

    mycursor = cnx.cursor()
    #pin = 4

    sql_select_Query = "select * from piSS_Zones Where Zone = 9999;"
    mycursor.execute(sql_select_Query)
    ReturnedStatus = mycursor.fetchone()

    databaseValue = ReturnedStatus[3]

    print('Begenning, ', databaseValue)

    print('Switch, ', DatabasePullStatus(databaseValue))
    #status = pifacedigital.input_pins[pin].value
    #pifacedigital.output_pins[pin].value = status
    #pifacedigital.leds[pin].toggle()
    #print(pin, 'is ', status, "record inserted.")
    #print('Database is ', databaseValue, 'and ', status, "is.")


    sql = "Update piSS_Zones Set Status = %d WHERE Zone BETWEEN 0 AND 9999;" % (DatabasePullStatus(databaseValue))
    mycursor.execute(sql)

    cnx.commit()
    #pifacedigital.output_pins[pin].toggle()
    beeper(DatabasePullStatus(databaseValue), 4, DatabasePullStatus(databaseValue))
    print("Finished insertion")

    logAlarming(9999, DatabasePullStatus(databaseValue))

def qqupdateDatabase(pin):
    #cnx = mysql.connector.connect(user='pmatest',password='dummypassword',host='127.0.0.1',database='piSecuritySystem')
    mycursor = cnx.cursor()

    status = pifacedigital.input_pins[pin].value

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()
    #pifacedigital.output_pins[pin].toggle()
    #pifacedigital.output_pins[pin].value = status
    print(status, "record inserted.")

    cursor = cnx.cursor()

    query = ("SELECT first_name, last_name, hire_date FROM employees "
             "WHERE hire_date BETWEEN %s AND %s")

    hire_start = datetime.date(1999, 1, 1)
    hire_end = datetime.date(1999, 12, 31)

    cursor.execute(query, (hire_start, hire_end))

    for (first_name, last_name, hire_date) in cursor:
      print("{}, {} was hired on {:%d %b %Y}".format(
        last_name, first_name, hire_date))

    cursor.close()
    cnx.close()

#
#
#
#
#
# Main application begins below.
# Connect to the database
cnx = mysql.connector.connect(user='pmatest',password='dummypassword',host='127.0.0.1',database='piSecuritySystem')
print("Database connected")
pifacedigital = pifacedigitalio.PiFaceDigital()

schedule.every(5).seconds.do(job)

while True:
    #time.sleep(1)
    #monitorZones()

    # Main application begins below.
    # Connect to the database

    #schedule.every().second.do(job)
    #schedule.every().day.at("10:30").do(job)

    schedule.run_pending()
    #time.sleep(1)

    #cnx = mysql.connector.connect(user='pmatest',password='dummypassword',host='127.0.0.1',database='piSecuritySystem')
    #print("Database connected")
    #pifacedigital = pifacedigitalio.PiFaceDigital()

    listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
    #listener5 = pifacedigitalio.InputEventListener(chip=pifacedigital)

    listener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall0)
    listener.register(1, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall1)
    listener.register(2, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall2)
    listener.register(3, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall3)

    #listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
    #listener5 = pifacedigitalio.InputEventListener(chip=pifacedigital)

    #beeper(1,1,0)

try:
    #listener.activate()
    print("All Activated")

    #databaseConnection = DatabaseCon()
    #databaseConnection.connect

except (KeyboardInterrupt, SystemExit):
    print("\n Ending Process")
    listener.deactivate()
    listener. destroy()
    cnx.close()