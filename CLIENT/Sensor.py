from sense_hat import SenseHat
import Client as cli

TOLERANCE = 2.0

y = (255,255,0) #sárga
b = (0,0,0) #fekete

run_pixels = [
        b,b,y,y,y,y,b,b,
        b,y,b,b,b,b,y,b,
        y,b,b,y,b,y,b,y,
        y,b,b,b,b,b,b,y,
        y,b,y,b,b,y,b,y,
        y,b,b,y,y,b,b,y,
        b,y,b,b,b,b,y,b,
        b,b,y,y,y,y,b,b
    ]

class SSense:
    
    def __init__(self, master = None):
        self.sense = SenseHat()
        self.sense.clear()

                

    def tempStr(self):
        return str(round(self.sense.get_temperature()))

    def humStr(self):
        return str(round(self.sense.get_humidity()))

    def onDisplay(self):
        self.sense.set_pixels(run_pixels)

    def offDisplay(self):
        self.sense.clear()

    def senseActivate(self,ttemp,thum):
        
        
        temperature = self.sense.get_temperature()
        if temperature <= (ttemp-TOLERANCE) or temperature >= (ttemp+TOLERANCE):
            if temperature < ttemp-TOLERANCE:
                cli.locSend("Fűtés!")
                print("Fűtés!")
            else:
                cli.locSend("Hűtés!")
                print("Hűtés!")
        humidity = self.sense.get_humidity()
        if humidity <= (thum-TOLERANCE) or humidity >= (thum+TOLERANCE):
            if humidity <= thum-TOLERANCE:
                cli.locSend("Párásítás!")
                print("Párásítás!")
            else:
                cli.locSend("párátlanítás!")
                print("Párátlanítás!")

'''
tempActivate(20.0,3.0)
humActivate(40.0,3.0)
'''
