import pifacedigitalio
import mysql.connector

#Define required functions...
def pause():
    programPause = input("Press the <ENTER> key to continue...")

def updateDatabase(pin):
    #cnx = mysql.connector.connect(user='pmatest',password='dummypassword',host='127.0.0.1',database='piSecuritySystem')
    mycursor = cnx.cursor()

    status = pifacedigital.input_pins[pin].value

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()
    pifacedigital.output_pins[pin].toggle()

def updateDatabase1(pin, status):
    #cnx = mysql.connector.connect(user='pmatest',password='dummypassword',host='127.0.0.1',database='piSecuritySystem')
    mycursor = cnx.cursor()

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()
    pifacedigital.output_pins[pin].toggle()

def updateDatabase2(pin):
    #cnx = mysql.connector.connect(user='pmatest',password='dummypassword',host='127.0.0.1',database='piSecuritySystem')
    mycursor = cnx.cursor()

    status = pifacedigital.input_pins[pin].value

    sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
    val = (str(pin), str(status))
    mycursor.execute(sql, val)

    cnx.commit()
    pifacedigital.output_pins[pin].value = status

# Main application begins below.
# Connect to the database
cnx = mysql.connector.connect(user='pmatest',password='dummypassword',host='127.0.0.1',database='piSecuritySystem')
print("Database connected")
pifacedigital = pifacedigitalio.PiFaceDigital()

listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
#listener2 = pifacedigitalio.InputEventListener(chip=pifacedigital)
#listener5 = pifacedigitalio.InputEventListener(chip=pifacedigital)

listener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, updateDatabase(0))
listener.register(1, pifacedigitalio.IODIR_FALLING_EDGE, updateDatabase(1))
listener.register(5, pifacedigitalio.IODIR_FALLING_EDGE, updateDatabase(5))

listener.activate()