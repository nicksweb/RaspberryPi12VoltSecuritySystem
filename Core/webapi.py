from flask import Flask
from functions import * 
app = Flask(__name__)

@app.route('/')
def hello():
     return "Hello World"     
     beeper(1,2,1)
     
@app.route('/api')
def zone0():
    RemoteInput7("run")
    return "Zone0"

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
    app.run(host='0.0.0.0')
    
