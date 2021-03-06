# functions.py
import globals
import alerts

# extras
import mysql.connector
import pifacedigitalio
import time
import mysql.connector
import threading
import datetime 

import requests

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
    x= 0 
    #if globals.delayArmingx == 0:
    #   globals.Arming_Delay = 1
        
    if (globals.Arming_Delay==1 and globals.AlarmCalled == 0):
        if globals.ArmingDelayRunning+globals.ArmingDelay < 60:
            globals.ArmingDelayRunning+=globals.ArmingDelay
            globals.runOnce_AlarmDelay = 1
        else:
            globals.ArmingDelayRunning=(60-globals.ArmingDelay)
            globals.runOnce_AlarmDelay = 1
        
    if(globals.Arming_Delay == 0 and x < globals.ArmingDelay+globals.ArmingDelayRunning and globals.AlarmCalled==0):
        # Prevent threads from being ran.     
        globals.Arming_Delay=1
        globals.runOnce_AlarmDelay=1
           
        #time.sleep(1)
        #log(str('Delaying Arming for approx:\t%d\t' % (globals.ArmingDelayRunning+globals.ArmingDelay)))

        while ( x < globals.ArmingDelayRunning+globals.ArmingDelay):    
            
            log(str('Delaying Arming for approx:\t%d\t<\t%d\t' % (x, globals.ArmingDelayRunning+globals.ArmingDelay)))
            x += 1
            time.sleep(1)
            
            log("In Delay Loop") 
                       
            if x == globals.ArmingDelayRunning+globals.ArmingDelay:
                globals.Arming_Delay=0
                globals.ArmingDelayRunning=0
                globals.AlarmCalled = 0
                #globals.delayArmingx = 0
                globals.runOnce_AlarmDelay = 0

def timerBeeper(timerDecimal):
        switcher={
            0: Decimal(0.5),
            1: Decimal(0.2)
        }
        return switcher.get(timerDecimal,"Invalid result fetches")

def AlarmDelayBeeper():
    globals.AlarmDelayBeeper = 1
    
    while globals.AlarmDelayBeeper==1:
        
        time.sleep(0.2)
        pifacedigital.output_pins[0].value = globals.ServiceMode #w
        pifacedigital.output_pins[2].value = globals.ServiceMode #w
        
        time.sleep(0.2)
        pifacedigital.output_pins[0].value = 0 #w
        pifacedigital.output_pins[2].value = 0 #w
        
        if globals.AlarmDelayBeeper==0:
            pifacedigital.output_pins[0].value = 0 #w
            pifacedigital.output_pins[2].value = 0 #w            

def beeper(w,x,timeChoice): # Number of times to beep
    # Do something
    timeVal = float(timerBeeper(timeChoice))

    log(str('\nBeeping:\t%d\t\n' % (x)))

    if(w == 0):     # Change timeVal to 0.5 so that when alarm is disabling it's a long beep.
        timeVal = float(0.5)
        # Short beeps remain the same at 0.2 (As per timerBeeper function above).
        w = 1 # Set w to 1 so output pin will be high (On)

    print("Before the 4 loop")

    for i in range(x):
        
        #print("Zone in Alarm - ", globals.ZoneinAlarm, "AlarmClear", globals.AlarmClear, " globals.StatusArmed - ", globals.arrayStatusArmed[globals.ZoneinAlarm])
        #if globals.ZoneinAlarm != 99:
        #    if  globals.AlarmClear==1 or globals.arrayStatusArmed[globals.ZoneinAlarm] == 0:
        #        pifacedigital.output_pins[0].value = 0
        #        pifacedigital.output_pins[2].value = 0
        #        return
                                
        #time.sleep(timeVal)
        time.sleep(timeVal)
        pifacedigital.output_pins[0].value = globals.ServiceMode #w
        pifacedigital.output_pins[2].value = 1 #w
        
        #if globals.ZoneinAlarm != 99:
        #    if  globals.AlarmClear==1 or globals.arrayStatusArmed[globals.ZoneinAlarm] == 0:
        #        pifacedigital.output_pins[0].value = 0
        #        pifacedigital.output_pins[2].value = 0
        #        return
            
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

    if zoneinfo[3] ==  1:
        aaEmailNotification = threading.Thread(target=sendNotification, 
        args=(8,'','','','','','','Zone %s is Armed' % zoneinfo[2],'Zone %s is Armed' % zoneinfo[2]))
        aaEmailNotification.start() 
    
    if zoneinfo[3] ==  0:
        aaEmailNotification = threading.Thread(target=sendNotification, 
        args=(8,'','','','','','','Zone %s is Disarmed' % zoneinfo[2],'Zone %s is Disarmed' % zoneinfo[2]))
        aaEmailNotification.start() 

def pirSensorLog(pin, status):
    
    if pin <= 40:
        if(globals.arrayStatusArmed[pin]==1 and globals.Arming_Delay==0):
            cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
            mycursor = cnx.cursor()
            sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
            val = (str(pin), str(status))
            mycursor.execute(sql, val)
            cnx.commit()
            log("Logging Motion Event")
            cnx.close()
    
    if pin >= 40:
            cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
            mycursor = cnx.cursor()
            sql = "INSERT INTO piSS_SensorLog (Port, Status) VALUES (%s, %s)"
            val = (str(pin), str(status))
            mycursor.execute(sql, val)
            cnx.commit()
            log("Logging Motion Event")
            cnx.close()

    #returnedStatus = getLastSensorLog(globals.ZoneinAlarm)
    zoneinfo = PISSZoneStatus(pin)
    log(str('\nMotion:\t%s\t\t%d \n' % (zoneinfo[2],status)))


def pirEventCall0(event):
    pin = 0
    status = pifacedigital.input_pins[pin].value
    #pirSensorLog(pin, status)
    if globals.AlarmCalled==0 and globals.Arming_Delay==0: checkZone(pin) 

def pirEventCall1(event):
    pin = 1
    status = pifacedigital.input_pins[pin].value
    #pirSensorLog(pin, status)
    if globals.AlarmCalled==0 and globals.Arming_Delay==0: checkZone(pin)

def pirEventCall2(event):
    pin = 2
    status = pifacedigital.input_pins[pin].value
    #pirSensorLog(pin, status)
    if globals.AlarmCalled==0 and globals.Arming_Delay==0: checkZone(pin)

def pirEventCall3(event):
    pin = 3
    status = pifacedigital.input_pins[pin].value
    #pirSensorLog(pin, status)
    if globals.AlarmCalled==0 and globals.Arming_Delay==0: checkZone(pin)
    
def pirEventCall4(event):
    pin = 4
    status = pifacedigital.input_pins[pin].value
    #pirSensorLog(pin, status)
    if globals.AlarmCalled==0 and globals.Arming_Delay==0: checkZone(pin)   

def wifiSensor(zoneID,arrayPos):
    if globals.AlarmCalled==0 and globals.Arming_Delay==0: checkZone(zoneID,arrayPos)  

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

def RemoteInput4(event): # D Key on Remote # Emergency Mode (Red Button)
    ScreamerStop()
    
    zone = 9998
    returnedStatus = remoteSensorLogSelect(zone)
    databaseValue = returnedStatus[3]

    PersonalEmergency(DatabasePullStatus(databaseValue))

    RemoteUpdateSingleZone(zone, DatabasePullStatus(databaseValue))
    #beeper(DatabasePullStatus(databaseValue), 4, DatabasePullStatus(databaseValue))
    logAlarming(9998, DatabasePullStatus(databaseValue))
    
     
def PersonalEmergency(x): 
      log(str('\n**** Emergency Mode ***'))
      log('\n\tAlarm Thread Starting.\n')
      
      globals.EmergencyActivated = x
      print(globals.EmergencyActivated, "Emergency Activated")
      
      if(x==1):
          ScreamerStart()                             
          globals.AlarmCalled=1
          aaEmailNotification = threading.Thread(target=sendNotification, 
          args=(3,'','','','','','','',''))
          aaEmailNotification.start()
          
      else:
          ScreamerStop()
          aa = threading.Thread(target=delayArming)
          #globals.thread_list.append(aa)  
          aa.start()
          #print("Alarm is muted")
          globals.AlarmCalled=0
          aaEmailNotification = threading.Thread(target=sendNotification, 
          args=(4,'','','','','','','',''))
          aaEmailNotification.start()
          
def IFTTTNotification(x=0): 
    
    globals.AlarmCalled=0
    globals.Arming_Delay=0
    
    if (globals.runIFTTTOnce==0):
        aa = threading.Thread(target=sendIFTTT)
        #globals.CurrentTriggers[zone] = 0     
        #globals.thread_list.append(aa)
        aa.start()
        globals.runIFTTTOnce=1

def RemoteInput5(event):  # C Key on remote.
    # Using for loop to loop through the C key zones.
    ScreamerStop()

    aa = threading.Thread(target=delayArming)
    #globals.thread_list.append(aa)
    aa.start()
    
    globals.keyC = DatabasePullStatus(globals.keyC)
       
    selected_elements = [globals.arrayStatusArmed[index] for index in globals.keyCList]   
       
    if max(selected_elements) > 0:
        globals.keyC = 0    
        globals.AlarmDelayBeeper = 0  
        
    for i in globals.keyCList:        
        if globals.AlarmDelayBeeper == 0: 
            beeper(globals.keyC,1,globals.keyC)            
        RemoteUpdateSingleZone(i, globals.keyC)            
        globals.arrayStatusArmed[i] = globals.keyC            
        logAlarming(i, globals.keyC)

       
def RemoteInput6(event): # B Key on remote.
    # Using for loop to loop through the B key zones.
    ScreamerStop()
    
    aa = threading.Thread(target=delayArming)
    #globals.thread_list.append(aa)
    aa.start()
    
    globals.keyB = DatabasePullStatus(globals.keyB)
    
    print("Zone Key Status B - %s" % globals.keyB)

    selected_elements = [globals.arrayStatusArmed[index] for index in globals.keyBList]
   
    if max(selected_elements) > 0:
        globals.keyB = 0
        globals.AlarmDelayBeeper = 0 

    #if max(globals.arrayStatusArmed) > 0:
    #    globals.keyB = 0  
    #    globals.AlarmDelayBeeper = 0        
        
    for i in globals.keyBList:        
        if globals.AlarmDelayBeeper == 0: 
            beeper(globals.keyB,1,globals.keyB)
        RemoteUpdateSingleZone(i, globals.keyB)            
        globals.arrayStatusArmed[i] = globals.keyB            
        logAlarming(i, globals.keyB)

       
def RemoteInput7(event): # A Key on remote.
    # Using for loop to loop through the A key zones.
    ScreamerStop()
    
    aa = threading.Thread(target=delayArming)
    #globals.thread_list.append(aa)
    aa.start()
    
    globals.keyA = DatabasePullStatus(globals.keyA)
    
    selected_elements = [ globals.arrayStatusArmed[index] for index in globals.keyAList ]
        
    if max(selected_elements) > 0:
        globals.keyA = 0
        globals.AlarmDelayBeeper = 0 
    
    #time.sleep(10)    
        
    for i in globals.keyAList:        
        globals.arrayStatusArmed[i] = globals.keyA
        
        if globals.AlarmDelayBeeper == 0: 
            beeper(globals.keyA,1,globals.keyA)
            
        RemoteUpdateSingleZone(i, globals.keyA)            
        logAlarming(i, globals.keyA)
                    
def initZones(): # Ran at program start-up to set all zones to off.
  RemoteUpdateSingleZone(0, 0)
  RemoteUpdateSingleZone(1, 0)
  RemoteUpdateSingleZone(2, 0)
  RemoteUpdateSingleZone(3, 0)
  RemoteUpdateSingleZone(5, 0)
  RemoteUpdateSingleZone(9999, 0)

# This zone checks if alarm should be activated and subsequently sounded.
def checkZone(zone,wifiDetail=0):
    
    zoneinfo = PISSZoneStatus(zone)
    
    print ("In CheckZone:", globals.arrayStatusArmed[zone], "   Alarm Delay", globals.alarm_delay)


    print(zoneinfo)

    if wifiDetail==0 and globals.arrayStatusArmed[zone] == 1 and globals.alarm_delay == 0: #or globals.arrayStatusArmed[9999] == 0:
        globals.CurrentTriggers[zone] += 1
        title = 'Triggered: %s Zone' % zoneinfo[2]
        message = 'Zone has been Triggered %s a total of %d times' % (zoneinfo[2],globals.CurrentTriggers[zone])
        aaEmailNotification = threading.Thread(target=sendNotification,args=(9,'','','','','','',title,message))
        aaEmailNotification.start()
        pirSensorLog(zone, 1)

    if wifiDetail>=1 and globals.arrayStatusArmed[wifiDetail] == 1 and globals.alarm_delay == 0 and globals.runIFTTTOnce==0: #or globals.arrayStatusArmed[9999] == 0:
        globals.CurrentTriggers[wifiDetail] += 1
        title = 'Triggered: %s Zone' % zoneinfo[2]
        message = 'Zone has been Triggered %s a total of %d times' % (zoneinfo[2],globals.CurrentTriggers[wifiDetail])
        aaEmailNotification = threading.Thread(target=sendNotification,args=(9,'','','','','','',title,message))
        aaEmailNotification.start()
        aaIFTTTNotification = threading.Thread(target=IFTTTNotification)
        globals.thread_list.append(aaIFTTTNotification)
        aaIFTTTNotification.start()
        pirSensorLog(zone, 1)        

    if zone in globals.reedSwitches:
        globals.CurrentTriggers[wifiDetail] = globals.MinAlarmTriggers+2 # So it trips the alarm instantly - It's a Reed Switch.       

    if wifiDetail==0:
        print("Current Trigers:",globals.CurrentTriggers[zone])
    
    if wifiDetail>=1:
        print("Current Trigers:",globals.CurrentTriggers[wifiDetail])

    log(str('\n%s Zone has triggered a checkZone()\n' % (zoneinfo[2])))

    #zone=wifiDetail

    # Could use global.ClearAlarm as a variable to switch a triggered alarm off and set CurrentTriggers to 0 (Restarting the detection process).
    if wifiDetail==0 and globals.arrayStatusArmed[zone] == 0 and globals.AlarmCalled == 0 and globals.run_once == 0:
       globals.CurrentTriggers[zone] = 0

    #if wifiDetail>0 and globals.arrayStatusArmed[wifiDetail] == 0 and globals.AlarmCalled == 0 and globals.run_once == 0:
    #   globals.CurrentTriggers[wifiDetail] = 0

    if wifiDetail==0 and sum(globals.CurrentTriggers) >= globals.MinAlarmTriggers and globals.AlarmCalled == 0 and globals.Arming_Delay == 0:
       globals.AlarmCalled=1

       #if wifiDetail>=1 and globals.runIFTTTOnce==0:
        #   globals.runIFTTTOnce=1
        #   globals.ZoneinAlarm=wifiDetail
        #   log(str('\n%s Zone has triggered %s activation of the Zone\'s sensor' % (str(zoneinfo[2]),str(globals.CurrentTriggers[wifiDetail]))))
        #   log('\n\tSending Notifcation with Notifcation Thread for a Wifi Action.\n')
           ### run
           #globals.CurrentTriggers = [0]*globals.AlarmsinUse
           #globals.AlarmTempMute = 0
           #globals.AlarmCalled=0
           #globals.run_once = 0
           #globals.ZoneinAlarm = 99
           #globals.AlarmClear = 0
           
           #aa = threading.Thread(target=ActivateAlarm, args=(zone,))
           #globals.CurrentTriggers[zone] = 0     
           #globals.thread_list.append(aa)
           #aa.start()
           
           #globals.AlarmCalled=0
           #globals.Arming_Delay=0
           #globals.AlarmClear=1
           
       if wifiDetail==0:
           globals.ZoneinAlarm=zone

           log(str('\n%s Zone has triggered %s activation of the Zone\'s sensor' % (str(zoneinfo[2]),str(globals.CurrentTriggers[zone]))))
           log('\n\tAlarm Thread Starting.\n')
           aa = threading.Thread(target=ActivateAlarm, args=(zone,))
           globals.CurrentTriggers[zone] = 0     
           globals.thread_list.append(aa)
           aa.start()
      
       

      # initZones()  Use only for testing - Used to set Database values back to 0 for Alarm's Activation Status - If using in producti on - Once alarm is activated
      #             It will not reactivate after it's first activation.


def ScreamerStart():
    # Screamer is 1 - External.
    # Internal is 4 - Internal Alarms
    pifacedigital.output_pins[1].value = globals.AlarmAudible # This would usually be one when not being tested. # Usually globals.AlarmAudible but not enough power... 
    pifacedigital.output_pins[4].value = globals.AlarmAudible
    log("\n\n\t\tSCREAMER IS ON!!!!!\n\n")
    # Output pin 3 is strobe on the flashing siren.
    pifacedigital.output_pins[3].value = 1
    # Output pin 2 is the solid light on the siren.
    pifacedigital.output_pins[2].value = 1
    #print("Alarm is sounding")
    time.sleep(1)
            
def ScreamerStop():
    # Mutes the Alarm if sounding for longer than AlarmTime (Refer to ScreamerControl)
    log("\n\n\t\tSCREAMER IS Off!!!!!\n\n")
    pifacedigital.output_pins[2].value = 0 # globals.AlarmAudible if you want the light to remain on after it's been triggered. 
    pifacedigital.output_pins[3].value = 0
    pifacedigital.output_pins[1].value = 0
    pifacedigital.output_pins[4].value = 0
    
def Screamer():

    time.sleep(1) # Short delay to let ScreamerControl Catch-up for AlarmDelay if used...

    while (globals.AlarmCalled == 1):  # Removed globals.AlarmAudible (globals.AlarmAudible==1 and )

        while (globals.Alarm_Delay==1): # and globals.AlarmCalled == 1):
            print("Screamer Waiting")
            time.sleep(1)

        while (globals.AlarmTempMute == 0 and globals.AlarmCalled == 1 and globals.Alarm_Delay==0):
            # Screamer is 1.
            pifacedigital.output_pins[1].value = globals.AlarmAudible # This would usually be one when not being tested. # Usually globals.AlarmAudible but not enough power... 
            log("\n\n\t\tSCREAMER IS ON!!!!!\n\n")
            # Output pin 3 is strobe on the flashing siren.
            pifacedigital.output_pins[3].value = 1
            pifacedigital.output_pins[4].value = globals.AlarmAudible
            # Output pin 2 is the solid light on the siren.
            pifacedigital.output_pins[2].value = 0
            #print("Alarm is sounding")
            time.sleep(0.1)

        while (globals.AlarmTempMute == 1 or globals.AlarmCalled == 1 and globals.Alarm_Delay==0):
            # Mutes the Alarm if sounding for longer than AlarmTime (Refer to ScreamerControl)
            log("\n\n\t\tSCREAMER IS Muted!!!!!\n\n")
            pifacedigital.output_pins[1].value = 0
            pifacedigital.output_pins[3].value = 0
            pifacedigital.output_pins[4].value = 0
            pifacedigital.output_pins[2].value = 1
            #print("Alarm is muted")
            time.sleep(0.1)

        log("ALarm Temp Mute: %d" % (globals.AlarmTempMute))
        log("ALarm Called: %d" % (globals.AlarmCalled))
        log("ALarm Called: %d" % (globals.Alarm_Delay))

    # Set Screamer to off just in case.
    pifacedigital.output_pins[0].value = 0
    pifacedigital.output_pins[1].value = 0
    pifacedigital.output_pins[2].value = 0
    pifacedigital.output_pins[3].value = 0
    pifacedigital.output_pins[4].value = 0

def ScreamerOff():
    pifacedigital.output_pins[1].value = 0
    pifacedigital.output_pins[2].value = 0 # Solid light
    pifacedigital.output_pins[3].value = 0 # Flashing Strobe Effect
    pifacedigital.output_pins[4].value = 0 # Flashing Strobe Effect
    # Screamer is now off.
    print("Alarm is off now...")
    #aa = threading.Thread(target=delayArming)
    #globals.thread_list.append(aa)
    #aa.start()

def ScreamerControl():

    x = 0

    log("Screamer Control %d %d %d " % (globals.AlarmDelay, globals.AlarmClear, globals.Alarm_Delay))

    while((globals.AlarmDelay*10) > x and globals.AlarmClear==0 and globals.Alarm_Delay==1 and globals.AlarmCalled == 1): # and globals.arrayStatusArmed[globals.ZoneinAlarm] == 1

        log("Delaying Alarm:\t%d" % ((globals.AlarmDelay*10)-x))


        #Start Beeper in separate thread so it does't slow this thread down.
        if (x == 0): # Only start the thread once.
            ad = threading.Thread(target=AlarmDelayBeeper)
            ad.start()

        x += 1

        if (globals.AlarmDelay*10) == x or globals.Alarm_Delay==0:
            x = 0 
            globals.Alarm_Delay = 0
            globals.AlarmTempMute = 0
            globals.AlarmDelayBeeper = 0
            log("Alarm_Delay finshed")

            returnedStatus = getLastSensorLog(globals.ZoneinAlarm)
            zoneinfo = PISSZoneStatus(globals.ZoneinAlarm)

            aaEmailNotification = threading.Thread(target=sendNotification, 
            args=(1,globals.ZoneinAlarm,"Urgent - Alarm Notifcation - " + str(returnedStatus[0]),
            "Zone " + str(zoneinfo[2]) + " is in Alarm",
            "Bryony Crt",
            "Time of Incident: " + str(returnedStatus[0]),
            globals.smtpEmail,'',''))
            globals.thread_list.append(aaEmailNotification)

            aaEmailNotification.start()

        time.sleep(0.1)

    globals.Alarm_Delay = 0
    globals.AlarmTempMute = 0
    globals.AlarmDelayBeeper = 0
    log("Alarm_Delay finshed")

    x = 0
    w = 0
    count = 0

    while (globals.AlarmCalled == 1 and globals.AlarmLoop >= x):
                     
        while (globals.AlarmCalled == 1 and (globals.AlarmTime*10) > count and globals.AlarmClear != 1):
            log("Alarm is Sounding... Sleeping Alarm for, %d seconds." % ((globals.AlarmTime*10)-count))
            count += 1
            time.sleep(0.1)
            
            if count == 1: 
                ScreamerStart()

        x += 1

        log("ALarm Loops Remaining: %d" % (globals.AlarmLoop-x))
        log("ALarm Called: %d" % (globals.AlarmCalled))

        print("Before end if statement", globals.AlarmLoop-x, " ", globals.AlarmCalled) 

        if ((globals.AlarmLoop-x)==0 or globals.AlarmCalled == 0 or globals.AlarmClear==1):
            ScreamerStop()
            globals.AlarmCalled = 0
            globals.AlarmTempMute = 0
            globals.run_once=0
            #globals.AlarmCalled = 0
            x = x + globals.AlarmLoop
            log("Alarm control has ended...")
            globals.CurrentTriggers = [0]*globals.AlarmsinUse
            #xxx
            break



def ActivateAlarm(name):
    # Initiate Class for Screamer...
    # Function is used so it can be cancelled easily.
    aaAlarmControl = threading.Thread(target=ScreamerControl)

    returnedStatus = getLastSensorLog(globals.ZoneinAlarm)
    zoneinfo = PISSZoneStatus(globals.ZoneinAlarm)

    setConfigurationSettings('ZoneinAlarm',globals.ZoneinAlarm)

    aaEmailNotification = threading.Thread(target=sendNotification, 
    args=(10,globals.ZoneinAlarm,"Urgent - Delay Notifcation - " + str(returnedStatus[0]),
    "Zone " + str(zoneinfo[2]) + " is in Delay",
    "Bryony Crt",
    "Time of Incident: " + str(returnedStatus[0]),
    globals.smtpEmail,'',''))

    print("At Activate Alarm")
    print(globals.AlarmCalled, " ", globals.run_once, " ", globals.AlarmClear, " ", globals.arrayStatusArmed[globals.ZoneinAlarm])

    while (globals.AlarmCalled==1 and globals.run_once == 0): # Don't need this anymore sum(globals.arrayStatusArmed) > 0 and ...
       # Do something...
       print("Waiting at alarm clear")
       x = 0

       if globals.run_once == 0 and globals.AlarmClear == 0 and globals.arrayStatusArmed[globals.ZoneinAlarm] == 1:
          log("Starting Alarm Threads - ActivateAlarm (True) - Run_Once")
          globals.thread_list.append(ScreamerControl)
          globals.thread_list.append(aaEmailNotification)
          #globals.AlarmAudible=getConfigurationSettingsValue(10001)

          globals.Alarm_Delay=1
          aaAlarmControl.start()
          aaEmailNotification.start()

          globals.run_once = 1

       while globals.AlarmCalled!=0 or globals.AlarmClear!=1 or globals.arrayStatusArmed[globals.ZoneinAlarm] != 0:
            
           if x==0: print("Waiting to Cancel the alarm")
           x += 1

           if (globals.AlarmCalled==0 or globals.AlarmClear==1 or globals.arrayStatusArmed[globals.ZoneinAlarm] == 0):
               print("Cancelling the alarm")
               ScreamerStop()
               #InfTimerScreamer.cancel()
               
               globals.CurrentTriggers = [0]*globals.AlarmsinUse
               globals.AlarmTempMute = 0
               globals.AlarmCalled=0
               globals.run_once = 0
               globals.ZoneinAlarm = 99
               
               ScreamerOff()
               setConfigurationSettingsInt(10003,0) # Update AlarmClear in DB.
               globals.Arming_Delay=0
               globals.Alarming_Delay=0
               globals.AlarmClear=0
               ScreamerOff()
               setConfigurationSettings('ZoneinAlarm',99)
               log("\n\tAlarm should now be off...")
               
               aaEmailNotification = threading.Thread(target=sendNotification, 
               args=(0,'','','','','','','',''))
               aaEmailNotification.start()
               #time.sleep(4)
               # Set Screamer to off.
               break
               #time.sleep(1)
               #time.sleep(0.1)

        # Send an email / SMS to the user / Whatapp / Singal Whatever is avaiable API wise.
        # Perhaps implement the DirectSMS API for messaging or similar.
        # Set of Screamer... for 5 mins...

def UpdateGlobals():
    start = time.time()

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
    globals.arrayStatusArmed[3]=databaseValue3
    
    returnedStatus = PISSZoneStatus(4)
    databaseValue5 = returnedStatus[3]
    globals.arrayStatusArmed[4]=databaseValue5

    returnedStatus = PISSZoneStatus(5)
    databaseValue5 = returnedStatus[3]
    globals.arrayStatusArmed[5]=databaseValue5
    
    returnedStatus = PISSZoneStatus(6)
    databaseValue5 = returnedStatus[3]
    globals.arrayStatusArmed[6]=databaseValue5

    #returnedStatus = PISSZoneStatus(9999)    For Tamper currently not implemented as 4 is being used for a sensor. 
    #databaseValue9x = returnedStatus[3]
    #globals.arrayStatusArmed[3]=databaseValue9x

    if (globals.Alarm_Delay==1 or globals.AlarmCalled == 1):
        globals.AlarmClear=getConfigurationSettingsValue(10003)

    end = time.time()
    print("Time taken for UpdateGlobals:", end-start)
        
def cron():
    start = time.time()

    globals.smtpEmail=getConfigurationSettingsValue('smtpEmail')
    globals.smtpUser=getConfigurationSettingsValue('smtpUser')
    globals.smtpPassword=getConfigurationSettingsValue('smtpPassword')
    globals.smtpServer=getConfigurationSettingsValue('smtpServer')
    globals.smtpPort=getConfigurationSettingsValue('smtpPort')
    globals.mailRecip=getConfigurationSettingsValue('mailRecip')
    globals.pushOverUserKey=getConfigurationSettings('pushOverUserKey')
    globals.pushOverAPPToken=getConfigurationSettings('pushOverAPPToken')
    globals.IFTTTAction=getConfigurationSettings('IFTTTAction')
    globals.EnableIFTTT=getConfigurationSettings('Enable_IFTTT')

    # Alarm Settings (Not critical)
    globals.MinAlarmTriggers=getConfigurationSettingsValue(10000)
    globals.AlarmAudible=getConfigurationSettingsValue(10001)
    globals.AlarmTime=getConfigurationSettingsValue(10002)
    globals.AlarmDelay=getConfigurationSettingsValue(10004)
    globals.AlarmLoop=getConfigurationSettingsValue(10005)
    globals.ArmingDelay=getConfigurationSettingsValue(10006)
    
    # Global Settings for System
    globals.SYSTEM_NAME=getConfigurationSettingsValue("SYSTEM_NAME")
    globals.ENABLE_EMAIL=getConfigurationSettingsValue("ENABLE_EMAIL")
    globals.ENABLE_PUSH=getConfigurationSettingsValue("ENABLE_PUSH")
    globals.ServiceMode=getConfigurationSettingsValue("ServiceMode")

    globals.pushURL=getConfigurationSettingsValue("pushURL")
    globals.webpathKey=getConfigurationSettingsValue("apiToken")
    
    globals.runIFTTTOnce=0

    end = time.time()
    print("Time taken for Cron:", end-start, "Service Mode - ", globals.ServiceMode)
    
def startup():
    # Run Cron to get App Settings
    cron()    
    aaEmailNotification = threading.Thread(target=sendNotification, 
    args=(2,'','','','','','','',''))
    aaEmailNotification.start()

def triggerReset():
    globals.CurrentTriggers = [0]*globals.AlarmsinUse
    print ("Reset Triggers", globals.CurrentTriggers)

def getConfigurationSettings(key): #Only ran once at program start-up and then every 30 minutes.
    sql = "select Value from piSS_Settings Where SettingKey = '%s';" % (key)
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchone()
    cnx.close()
    return result

def getConfigurationSettingsValue(key): #Only ran once at program start-up and then every 30 minutes.
    sql = "select Value from piSS_Settings Where SettingKey like '%s';" % (key)
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchone()
    cnx.close()
    return result[0]

def setConfigurationSettings(key,value):
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    sql = "Update piSS_Settings Set Value=%s Where SettingKey=%s;"
    val = (value, key)
    mycursor.execute(sql, val)
    cnx.commit()
    cnx.close()

def setConfigurationSettingsInt(key,value):
    cnx = mysql.connector.connect(user=globals.dbUser,password=globals.dbPassword,host=globals.dbHost,database=globals.dbDatabase)
    mycursor = cnx.cursor()
    sql = "Update piSS_Settings Set Value=%d Where SettingKey like %d;" % (int(value), int(key))
    #val = (value, key)
    mycursor.execute(sql)#, val)
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
        now=datetime.datetime.now()
        print(now," : ",name)


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
            


