from flask import Flask, request
from OpenSSL import SSL
from functions import *
#from functions import *

import os
context=SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join(os.path.dirname(__file__),'piss.crt') 
key = os.path.join(os.path.dirname(__file__),'piss.key')
app = Flask(__name__)

@app.route('/')
def hello():
     return globals.webpathKey
     #return "PiSSWeb"
     beeper(1,2,1)
     
@app.route('/'+ globals.webpathKey +'/RemoteInput4')
def zone4():
        RemoteInput4("run")
        return "RemoteInput4"

@app.route('/'+ globals.webpathKey +'/RemoteInput5')
def zone5():
        RemoteInput5("run")
        return "RemoteInput5"

@app.route('/'+ globals.webpathKey +'/RemoteInput6')
def zone6():
        RemoteInput6("run")
        return "RemoteInput6"
    
@app.route('/'+ globals.webpathKey +'/RemoteInput7')
def zone7():
        RemoteInput7("run")
        return "RemoteInput7"

@app.route('/'+ globals.webpathKey +'/AlarmClear')
def alarmClr():
        globals.AlarmClear=1
        return "AlarmClear=1"

@app.route('/'+ globals.webpathKey +'/ZoneControl')
def zone7x():
    if request.args.get('mode') == 'true': 
        zone = request.args['zone']
        RemoteUpdateSingleZone(int(zone),1)
        return zone
    else:
        zone = request.args['zone']
        RemoteUpdateSingleZone(int(zone),0)
        return zone

     
if __name__ == '__main__':
    globals.context=(globals.cer,globals.key)
    #app.run(host='0.0.0.0',port=5001,ssl_context=globals.context,debug=True)
    #app.run(host='0.0.0.0',port=5001,ssl_context='adhoc',debug=True) #
    #app.run(host='0.0.0.0',debug=True) 
    # // Guide for SSL blog.miguelgrinberg.com/post/running-your-flask-application-over-https
    
