# main.py
# Output to outputs on the PiAlarmSystem.

# Import Statements
import globals # Import globals.py
import monitor
#import mysql.connector

# Import functions.py
from functions import *

# Main application begins below.
# Connect to the database
listener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall0)
listener.register(1, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall1)
listener.register(2, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall2)
listener.register(3, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall3)
listener.register(4, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput4)
listener.register(5, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput5)
listener.register(6, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput6)
listener.register(7, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput7)

# Beep is a notification to confirm that the system is functioning.
beeper(1,1,1)

try:
    listener.activate()
    print("All Activated")

# Close Database and destroy listeners.
except (KeyboardInterrupt, SystemExit):
    print("\n Ending Process")
    listener.deactivate()
    listener. destroy()
    cnx.close()