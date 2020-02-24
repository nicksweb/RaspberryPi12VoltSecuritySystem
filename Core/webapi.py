from flask import Flask
from functions import * 
app = Flask(__name__)

@app.route('/')
def hello():
     return "Hello World"     
     beeper(1,2,1)
     
@app.route('/zone0')
def run():
    RemoteInput7("run")
    return "Zone0"
    
@app.route('/beep')
def hello2():
     beeper(1,2,1)
     return "Hello World2"     
     
     
     
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
