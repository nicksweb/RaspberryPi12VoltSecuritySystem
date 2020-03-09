from flask import Flask
from OpenSSL import SSL
#from functions import *

import os
context=SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join(os.path.dirname(__file__),'piss.crt') 
key = os.path.join(os.path.dirname(__file__),'piss.key')
app = Flask(__name__)

@app.route('/')
def hello():
     return "Hello World"     
     beeper(1,2,1)
     
@app.route('/RemoteInput4')
def zone4():
    RemoteInput4("run")
    return "Zone4"

@app.route('/RemoteInput5')
def zone5():
    RemoteInput5("run")
    return "Zone5"

@app.route('/RemoteInput6')
def zone6():
    RemoteInput6("run")
    return "Zone6"
    
@app.route('/RemoteInput7')
def zone7():
    RemoteInput7("run")
    return "Zone7"
     
     
if __name__ == '__main__':
    globals.context=(globals.cer,globals.key)
    app.run(host='0.0.0.0',port=5001,ssl_context=globals.context,debug=True)
    #app.run(host='0.0.0.0',port=5001,ssl_context='adhoc',debug=True) #
    #app.run(host='0.0.0.0') #
    # // Guide for SSL blog.miguelgrinberg.com/post/running-your-flask-application-over-https
    
