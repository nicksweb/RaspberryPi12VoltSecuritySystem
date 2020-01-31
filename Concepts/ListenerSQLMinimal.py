import time
import pifacedigitalio
import mysql.connector
from decimal import *

#Database Details
dbUser='pmatest'
dbPassword='dummypassword'
dbHost='127.0.0.1'
dbDatabase='piSecuritySystem'

###
###
## Classes to be used..
###
###
class Pissalarm:
    pin = 0
    type = "PIR"

    def summary(self):
        print("Type of Alarm: " + self.type + ", Pin: " + str(self.pin))

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

def pause():
    programPause = input("Press the <ENTER> key to continue...")

def logAlarming(pin, status):
    mycursor = cnx.cursor()

    #status = pifacedigital.input_pins[pin].value

    sql = "INSERT INTO piSS_Log_Arming (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)
    cnx.commit()

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

def RemoteInput4(event): # D Key on Remote
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

def RemoteInput5(event): # C Key on Remote
    mycursor = cnx.cursor()

    #pin = 5

    sql_select_Query = "select * from piSS_Zones Where Zone = 2;"
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


    sql = "Update piSS_Zones Set Status = %d WHERE Zone = 2" % (DatabasePullStatus(databaseValue))
    mycursor.execute(sql)

    cnx.commit()
    #pifacedigital.output_pins[pin].toggle()
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
    #status = pifacedigital.input_pins[pin].value
    #pifacedigital.output_pins[pin].value = status
    #pifacedigital.leds[pin].toggle()
    #print(pin, 'is ', status, "record inserted.")
    #print('Database is ', databaseValue, 'and ', status, "is.")


    sql = "Update piSS_Zones Set Status = %d WHERE Zone = 1" % (DatabasePullStatus(databaseValue))
    mycursor.execute(sql)

    cnx.commit()
    #pifacedigital.output_pins[pin].toggle()
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
    #status = pifacedigital.input_pins[pin].value
    #pifacedigital.output_pins[pin].value = status
    #pifacedigital.leds[pin].toggle()
    #print(pin, 'is ', status, "record inserted.")
    #print('Database is ', databaseValue, 'and ', status, "is.")


    sql = "Update piSS_Zones Set Status = %d WHERE Zone = 0" % (DatabasePullStatus(databaseValue))
    mycursor.execute(sql)

    cnx.commit()
    #pifacedigital.output_pins[pin].toggle()
    beeper(DatabasePullStatus(databaseValue), 1, DatabasePullStatus(databaseValue))
    print("Finished insertion")

    logAlarming(0, DatabasePullStatus(databaseValue))

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

# Main application begins below.
# Connect to the database
cnx = mysql.connector.connect(user='pmatest',password='dummypassword',host='127.0.0.1',database='piSecuritySystem')
print("Database connected")
pifacedigital = pifacedigitalio.PiFaceDigital()

listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
#listener5 = pifacedigitalio.InputEventListener(chip=pifacedigital)

listener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall0)
listener.register(1, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall1)
listener.register(2, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall2)
listener.register(3, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall3)
listener.register(4, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput4)
listener.register(5, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput5)
listener.register(6, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput6)
listener.register(7, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput7)

beeper(1,1,1)

try:
    listener.activate()
    print("All Activated")

    a1 = Pissalarm()
    a1.pin = 0

    a1.summary()

    databaseConnection = DatabaseCon()
    databaseConnection.connect

except (KeyboardInterrupt, SystemExit):
    print("\n Ending Process")
    listener.deactivate()
    listener. destroy()
    cnx.close()