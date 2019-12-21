# Import necessary modules.
from datetime import datetime as d
import datetime
import time
import pifacedigitalio
import pifacedigitalio as p
import mysql.connector

try:
    cnx = mysql.connector.connect(user='pmatest',password='dummypassword',host='127.0.0.1',database='piSecuritySystem')
except mysql.connector.Error as err:
   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
       print("Something is wrong with your user name or password")
   elif err.errno == errorcode.ER_BAD_DB_ERROR:
       print("Database does not exist")
   else:
       print(err)
else:
  print("Database connection successful")


pfd = pifacedigitalio.PiFaceDigital()

nowtime = d.now()

def Sleeper():
    while True:
        #Get user input

        #print('Alarm sensors are not active')

        time.sleep(.5)
        output = ''
        pinNum=9

        if p.digital_read(0) == 0:
            print('Sensor 0 is active.', currentDateTime())
            output = 0
            pinNum= 0
            writeInfo(pinNum, output)

        if p.digital_read(1) == 0:
            print('Sensor 1 is active.', currentDateTime())
            output = 0
            pinNum = 1
            writeInfo(pinNum, output)

        if p.digital_read(4) == 1:
            print('Sensor 4 is active.', currentDateTime())
            output = 1
            pinNum = 4
            writeInfo(pinNum, output)



def currentDateTime():
    nowtime = d.now()
    return nowtime.strftime("%Y-%m-%d %H:%M:%S")

def prepareFile():
    f = open('/home/pi/Documents/Python/PiAlarmSystem/DataDump.txt','a')
    f.write('\n' + "Commencing monitoring\n")
    f.close

def writeInfo(output, pinNum):
    f = open('/home/pi/Documents/Python/PiAlarmSystem/DataDump.txt','a')

    mycursor = cnx.cursor()

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = ('1', '0')
    mycursor.execute(sql, val)

    #f.write('"'+pinNum+'"')
    f.close

    cnx.commit()

    print(mycursor.rowcount, "record inserted.")

try:
    time.sleep(2)
    p.init()
    prepareFile()
    Sleeper()
except KeyboardInterrupt:
    print('Program exiting')
    cnx.close()
    exit()