import pifacedigitalio

def toggle_led0(event):
    event.chip.leds[0].toggle()

def toggle_led1(event):
    event.chip.leds[1].toggle()

def toggle_led5(event):
    event.chip.leds[5].toggle()

pifacedigital = pifacedigitalio.PiFaceDigital()

listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
listener2 = pifacedigitalio.InputEventListener(chip=pifacedigital)
listener5 = pifacedigitalio.InputEventListener(chip=pifacedigital)

listener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, toggle_led0)
listener2.register(1, pifacedigitalio.IODIR_FALLING_EDGE, toggle_led1)
listener5.register(5, pifacedigitalio.IODIR_FALLING_EDGE, toggle_led5)

listener.activate()
listener2.activate()
listener5.activate()