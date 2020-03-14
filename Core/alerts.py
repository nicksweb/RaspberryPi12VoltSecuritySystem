# functions.py
import globals
import http.client
#import urllib
import functions

#import pushover
#from pushover import init, Client
from pushover import Pushover

# From Github (https://github.com/dimaba/sendmail)
from sendmail import MailSender

PUSHOVER_TOKEN = { 'token' : globals.pushOverAPPToken[0]}
PUSHOVER_USER = { 'user' : globals.pushOverUserKey[0]}



#Pushover.__init__globals.pushOverAPPToken[0])
#Client(globals.pushOverUserKey[0]).send_message("PiSS has Started", title="PiSS is Running")

def sendNotification(Messagetype, zonenumber, title, subject, mailFrom, messageDetail, mailTo):

    GETLASTLog=functions.getLastSensorLog(globals.ZoneinAlarm)
    zoneinfo = functions.PISSZoneStatus(globals.ZoneinAlarm)

    if (globals.ENABLE_PUSH==1):
        po = Pushover(globals.pushOverAPPToken[0])
        po.user(globals.pushOverUserKey[0])   

        msg=po.msg("PiSS")
        
        msg.set("html",1)
        
        if Messagetype == 0:  
            msg.set("title", globals.pushsmtpTitle[0] % globals.SYSTEM_NAME)
            msg.set("message", globals.pushsmtpMessages[0])
        if Messagetype == 1:
            msg.set("title", globals.pushsmtpTitle[1] % (globals.SYSTEM_NAME,zoneinfo[2]))
            msg.set("message", globals.pushsmtpMessages[1] % zoneinfo[2])
            msg.set("priority","1")
            msg.set("retry","60")
            msg.set("sound","siren")
            msg.set("expire","3600")
        if Messagetype == 2:
            msg.set("title", globals.pushsmtpTitle[2] % globals.SYSTEM_NAME)
            msg.set("message", globals.pushsmtpMessages[2] % globals.SYSTEM_NAME)
        if Messagetype == 3:
            msg.set("title", globals.pushsmtpTitle[3] % (globals.SYSTEM_NAME))
            msg.set("message", globals.pushsmtpMessages[3])
            msg.set("priority","1")
            msg.set("retry","60")
            msg.set("sound","siren")
            msg.set("expire","3600")
        if Messagetype == 4:
            msg.set("title", globals.pushsmtpTitle[4] % (globals.SYSTEM_NAME))
            msg.set("message", globals.pushsmtpMessages[4])
            msg.set("priority","1")
            msg.set("retry","60")
            msg.set("sound","siren")
            msg.set("expire","3600")
          
        msg.set("url",globals.pushURL)

        po.send(msg)
        
    if (globals.ENABLE_EMAIL==1):
        ourmailsender = MailSender(globals.smtpUser[0], globals.smtpPassword[0], (globals.smtpServer[0], globals.smtpPort[0]))
        
        if Messagetype == 0:  
            #Do NOthing
            return
            
        if Messagetype == 1:
            subject = globals.pushsmtpTitle[1] % (globals.SYSTEM_NAME,zoneinfo[2])
            messageDetail = globals.pushsmtpMessages[1] % zoneinfo[2]
            plaintext = "Alarm Notification - Zone: " +  zoneinfo[2] + " , \n" \
                "Time of Event - \n" + str(GETLASTLog[0]) + " \n" \
                "" + messageDetail + "\n" + \
                " Status=" + str(GETLASTLog[1]) + \
                "\n" + subject + ""  
            ourmailsender.set_message(plaintext, subject, globals.SYSTEM_NAME)
            ourmailsender.set_recipients(globals.mailRecip) # Don't need to specify address in array as it's already in that format (a turple)
            ourmailsender.connect()
            ourmailsender.send_all()
