# main.py
# Output to outputs on the PiAlarmSystem.

# Import Statements
import globals # Import globals.py
import monitor

# Import functions, alerts
from functions import *
from alerts import * 
from webapi import *

# Main application begins below.
# Connect to the database

listener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall0) # Falling is for a PIR
listener.register(1, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall1)
listener.register(2, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall2)
listener.register(3, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall3)   #Rising is for a Reed Switch (A Switch basically!)
# Will now be a PIR for monitoring purposes... 
#listener.register(5, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput4)   #Disconnecting Key C for extra PIR 
listener.register(4, pifacedigitalio.IODIR_FALLING_EDGE, pirEventCall4)
listener.register(5, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput4) # Key D 
listener.register(6, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput6) # Key B 
listener.register(7, pifacedigitalio.IODIR_FALLING_EDGE, RemoteInput7) # Key A

# Beep is a notification to confirm that the system is functioning.
#beeper(1,1,1)
#initZones() #InitZones - Sets zones in the Database to an initival value of 0 - May disable this in future release but for now leaving in.
#beeper(1,2,1)

# Updates Global Variables and keeps what's needed in Sync with the Database.
t = InfiniteTimer(2, UpdateGlobals)
s = InfiniteTimer(45, cron)
r = InfiniteTimer(180, triggerReset)

# Download SMTP Server settings from the server - Currently it only calls this once on start-up.
globals.pushOverUserKey=getConfigurationSettings('pushOverUserKey')
globals.pushOverAPPToken=getConfigurationSettings('pushOverAPPToken')
globals.webpathKey=getConfigurationSettingsValue('apiToken')

try:
    listener.activate()
    startup()
    t.start()
    s.start()
    r.start()
    globals.context=(globals.cer,globals.key)
    app.run(host='0.0.0.0',port=5001,debug=False,use_reloader=False) 
    #app.run(host='0.0.0.0',port=5001,ssl_context=globals.context,debug=False,use_reloader=False) 
    #app.run(host='0.0.0.0')


# Close Database and destroy listeners.
except (KeyboardInterrupt, SystemExit):
    print("\n Ending Process")
    listener.deactivate()
    #listener.destroy()
    t.cancel()
    #cnx.close()
