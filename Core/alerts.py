# functions.py
import globals
#import functions as f1

#from functions import *
# From Github (https://github.com/dimaba/sendmail)
from sendmail import MailSender

def sendNotification(title, subject, mailFrom, messageDetail, mailTo):
    # Python Functions for Sending Alerts
    ourmailsender = MailSender(globals.smtpUser[0], globals.smtpPassword[0], (globals.smtpServer[0], globals.smtpPort[0]))

    plaintext = "Alarm Notification - Zone: " +  title + " , \n" \
            "Zone is in alarm state.\n" \
            "" + messageDetail + "" \
            "" + subject + ""

    #plaintext = "Alarm Notifcation Test"

    ourmailsender.set_message(plaintext, title, mailFrom)

    ourmailsender.set_recipients(globals.mailRecip) # Don't need to specify address in array as it's already in that format (a turple)

    ourmailsender.connect()
    ourmailsender.send_all()
