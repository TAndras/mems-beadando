import tkinter as tk
from Sensor import SSense
import sched, time
import _thread
import sys


class SenseSystem(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self,master)
        
        self.scan = SSense()
        
        self.uitemp = tk.StringVar()
        self.uihum = tk.StringVar()
        self.qtemp = tk.StringVar()
        self.qhum = tk.StringVar()
        self.auto = False
        
        self.grid()
        self.createWidgets()
        
    
    def createWidgets(self):
        
        
        self.tempUILabel = tk.Label(self, text = "Hőmérséklet")
        self.tempUILabel.grid(row = 0, column = 0)
        
        okaytemp = self.register(self.validateTemp)
        self.tempUIEntry = tk.Entry(self, textvariable = self.uitemp, validate = 'key', validatecommand = (okaytemp,'%i','%S','%P') )
        self.tempUIEntry.grid(row = 0, column = 1, columnspan = 2)
        
        self.humUILabel = tk.Label(self, text = "Páratartalom")
        self.humUILabel.grid(row = 1, column = 0)
        
        okayhum = self.register(self.validateHum)
        self.humUIEntry = tk.Entry(self, textvariable = self.uihum, validate = 'key', validatecommand = (okayhum,'%P'))
        self.humUIEntry.grid(row = 1, column = 1, columnspan = 2)
        
        self.qtempEntry = tk.Entry(self, textvariable = self.qtemp, state = 'disabled')
        self.qtempEntry.grid(row = 2, column = 1, columnspan = 2)
        
        self.qtempButton = tk.Button(self, text="Hőnérés",command = lambda: self.qtemp.set(self.scan.tempStr() + ' C'))
        self.qtempButton.grid(row = 2, column = 0)
        
        self.qhumEntry = tk.Entry(self, textvariable = self.qhum, state = 'disabled')
        self.qhumEntry.grid(row = 3, column = 1, columnspan = 2)
        
        self.qhumButton = tk.Button(self, text = "Páratartalom" ,command = lambda: self.qhum.set(self.scan.humStr() + ' %'))
        self.qhumButton.grid(row = 3, column = 0)
        
        self.startButton = tk.Button(self, text = "Start", command = lambda: self.autoRun(self.getuiTemp(),self.getuiHum() ) )
        self.startButton.grid(row = 4, column = 0)
        
        self.stopButton = tk.Button(self, text = "Stop", command = lambda: self.stop())
        self.stopButton.grid(row = 4, column = 2)
        
        self.quitButton = tk.Button(self, text = "Kilép", command = lambda: sys.exit())
        self.quitButton.grid(row = 4, column = 1)
    
    def getuiTemp(self):
        try:
           return float(self.tempUIEntry.get())
        except:
            print("Hibás \"Hőmérséklet\" bemenet! 0-val számol!")
            return 0.0
        
    def getuiHum(self):
        try:
            return float(self.humUIEntry.get())
        except:
            print("Hibás \"Páratartalom\" bemenet! 0-val számol!")
            return 0.0
        
    #adatbevitel vizsgálat (hőmérséklet)
    def validateTemp(self,index,input,newVal):
        if newVal == "" or newVal == "-":
            return True
        else:
            try:
                int(input)
                return True
            except:
                return False
        
    #adatbevitelvizsgálat (páratartalom)
    def validateHum(self,newVal):
        if newVal == "":
            return True
        try:
            check = int(newVal)
            if check >= 0 and check <= 100:
                return True
            else:
                return False
        except:
            return False
        
    def stop(self):
        self.auto = False
    
    def autoRun(self,ttemp,thum):
        if self.auto == False:
            print("START!")
            self.auto = True
            try:
                _thread.start_new_thread(self.cycle,(ttemp,thum))
            except:
                print("Szálhiba!")
        return True
    
    def cycle(self,ttemp,thum):
        self.scan.onDisplay()
        sch = sched.scheduler(time.time,time.sleep)
        while self.auto:
            sch.enter(10,1,self.scan.senseActivate, kwargs= {'ttemp': ttemp,'thum': thum})
            sch.run()
        self.scan.offDisplay()
        print("autómata működés megállítva!")
        
    