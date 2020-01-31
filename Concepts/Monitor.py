import time
import pifacedigitalio
import mysql.connector
from decimal import *

#Database Details
dbUser='pmatest'
dbPassword='dummypassword'
dbHost='127.0.0.1'
dbDatabase='piSecuritySystem'

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

while True:
    time.sleep(2)
    print("Looping")

    monitorZones()

#listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
#listener5 = pifacedigitalio.InputEventListener(chip=pifacedigital)

#beeper(1,1,0)

try:
    #listener.activate()
    print("All Activated")

    databaseConnection = DatabaseCon()
    databaseConnection.connect

except (KeyboardInterrupt, SystemExit):
    print("\n Ending Process")
    listener.deactivate()
    listener. destroy()
    cnx.close()