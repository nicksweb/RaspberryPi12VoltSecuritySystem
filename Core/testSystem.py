# functions.py
import globals
import time
import pdb

# extras
import pifacedigitalio

# Global Variables for PiFaceDigitalIO
# Used for Interacting/Interfacing
pifacedigital = pifacedigitalio.PiFaceDigital()
listener = pifacedigitalio.InputEventListener(chip=pifacedigital)

#
# PiFaceDigitalIO Functions
#
#Define required functions...

def starttest():        
    print("Testing the Beeper - Pin 0")
    key_pressed = input('Press ENTER to continue: ')

    pifacedigital.output_pins[0].value = 1 #w
    pifacedigital.output_pins[2].value = 1 #w
    
    time.sleep(0.1)
    
    pifacedigital.output_pins[0].value = 0 #w
    pifacedigital.output_pins[2].value = 0 #w
    
    print("Testing the External Siren - Pin 1")
    key_pressed = input('Press ENTER to continue: ')
    
    pifacedigital.output_pins[1].value = 1 #w
    pifacedigital.output_pins[2].value = 1 #w
    
    time.sleep(0.1)
    
    pifacedigital.output_pins[1].value = 0 #w
    pifacedigital.output_pins[2].value = 0 #w
    
    print("Testing the Solid Light on Small Sirens - Pin 2")
    key_pressed = input('Press ENTER to continue: ')
    
    pifacedigital.output_pins[2].value = 1 #w
    
    time.sleep(0.1)
    
    pifacedigital.output_pins[2].value = 0 #w
    
    print("Testing the Strobe on Front Siren - Pin 3")
    key_pressed = input('Press ENTER to continue: ')
    
    pifacedigital.output_pins[3].value = 1 #w
    pifacedigital.output_pins[2].value = 1 #w
    
    time.sleep(0.1)
    
    pifacedigital.output_pins[3].value = 0 #w
    pifacedigital.output_pins[2].value = 0 #w
    
    print("Testing the Internal Screamer - Pin 4")
    key_pressed = input('Press ENTER to continue: ')
    
    pifacedigital.output_pins[4].value = 1 #w
    pifacedigital.output_pins[2].value = 1 #w
    
    time.sleep(0.1)
    
    pifacedigital.output_pins[4].value = 0 #w
    pifacedigital.output_pins[2].value = 0 #w    

    print("Currently Unassigned - Pin 5")
    key_pressed = input('Press ENTER to continue: ')
    
    pifacedigital.output_pins[5].value = 1 #w
    pifacedigital.output_pins[2].value = 1 #w
    
    time.sleep(0.1)
    
    pifacedigital.output_pins[5].value = 0 #w
    pifacedigital.output_pins[2].value = 0 #w  
    
    print("Currently Unassigned - Pin 6")
    key_pressed = input('Press ENTER to continue: ')
    
    pifacedigital.output_pins[6].value = 1 #w
    pifacedigital.output_pins[2].value = 1 #w
    
    time.sleep(0.1)
    
    pifacedigital.output_pins[6].value = 0 #w
    pifacedigital.output_pins[2].value = 0 #w   

    print("Currently Unassigned - Pin 7")
    key_pressed = input('Press ENTER to continue: ')
    
    pifacedigital.output_pins[7].value = 1 #w
    pifacedigital.output_pins[2].value = 1 #w
    
    time.sleep(0.1)
    
    pifacedigital.output_pins[7].value = 0 #w
    pifacedigital.output_pins[2].value = 0 #w    

starttest() 
