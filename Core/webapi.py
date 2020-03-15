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
     return "PiSSWeb"     
     beeper(1,2,1)
     
@app.route('/'+ globals.webpathKey +'/RemoteInput4')
def zone4():
    
    if request.args.get('mode') == 'true':
        RemoteInput7("run")
        return "Zone4"
    else:
        return "Zone4-Off" 

@app.route('/'+ globals.webpathKey +'/RemoteInput5')
def zone5():
    
    if request.args.get('mode') == 'true':
        RemoteInput7("run")
        return "Zone5"
    else:
        return "Zone5-Off" 

@app.route('/'+ globals.webpathKey +'/RemoteInput6')
def zone6():
    
    if request.args.get('mode') == 'true':
        RemoteInput7("run")
        return "Zone6"
    else:
        return "Zone6-Off" 
    
@app.route('/'+ globals.webpathKey +'/RemoteInput7')
def zone7():
    
    if request.args.get('mode') == 'true':
        RemoteInput7("run")
        return "Zone7"
    else:
        return "Zone7-Off" 

@app.route('/'+ globals.webpathKey +'/RemoteInput7x')
def zone7x():
    
    if request.args.get('mode') == 'true':
        RemoteInput7("run")
        return "Zone7"
    else:
        return "Zone7-Off"   
     
if __name__ == '__main__':
    globals.context=(globals.cer,globals.key)
    app.run(host='0.0.0.0',port=5001,ssl_context=globals.context,debug=True)
    #app.run(host='0.0.0.0',port=5001,ssl_context='adhoc',debug=True) #
    #app.run(host='0.0.0.0') #
    # // Guide for SSL blog.miguelgrinberg.com/post/running-your-flask-application-over-https
    
