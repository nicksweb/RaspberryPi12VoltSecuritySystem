# functions.py
import globals
import http.client
import urllib
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
            
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": "",                       # Insert app token here
        "user": "",                       # Insert user token here
        "html": "1",                                # 1 for HTML, 0 to disable
        "title": "Motion Detected!",                # Title of the message
        "message": "<b>Front Door</b> camera!",     # Content of the message
        "url": "http://IP.ADD.RE.SS",               # Link to be included in message
        "url_title": "View live stream",            # Text for the link
        "sound": "siren",                           # Define the sound played
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

    #plaintext = "Alarm Notifcation Test"

    #ourmailsender.set_message(plaintext, title, mailFrom)

    #ourmailsender.set_recipients(globals.mailRecip) # Don't need to specify address in array as it's already in that format (a turple)

    #ourmailsender.connect()
    #ourmailsender.send_all()
    
    
