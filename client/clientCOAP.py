from coapthon.client.helperclient import HelperClient
from threading import Thread
import kitchen
import living_room
import utility_room
import bedroom
import bathroom
import outside
from tools import color
from Tkinter import *
import json
import ast
import time

host = "127.0.0.1"
port = 3005
client = HelperClient(server=(host, port))
client.put("resources","")
home = ast.literal_eval(client.get("resources").payload)
print(home)

bathroom.lightB = home['lightB']
bathroom.shower = home['shower']
bedroom.lightR1 = home['lightR1']
bedroom.lightR2 = home['lightR2']
bedroom.curtain = home['curtain']
kitchen.lightK = home['lightK']
kitchen.hood = home['hood']
kitchen.cooker = home['cooker']
kitchen.sink = home['sink']
living_room.tv = home['tv']
living_room.fan = home['fan']
living_room.lightL = home['lightL']
living_room.tempLimit = home['tempLimit']
utility_room.lightU = home['lightU']
utility_room.machine = home['machine']
outside.lightO = home['lightO']
#alarm = home['alarm']
outside.door = home['door']
outside.lock = home['lock']
labelTAct = ""

def GUI():
    fenetre = Tk()

    label = Label(fenetre, text="Smart Home")
    label.pack()
    buttonLL = Button(fenetre, text="living_room light", fg=color(living_room.lightL), command= lambda: living_room.living_room("lightL",client,buttonLL))
    buttonLL.pack()
    buttonLF = Button(fenetre, text="living_room fan", fg=color(living_room.fan),command= lambda: living_room.living_room("fan",client,buttonLF))
    buttonLF.pack()
    buttonLT = Button(fenetre, text="living_room tv", fg=color(living_room.tv),command= lambda: living_room.living_room("tv",client,buttonLT))
    buttonLT.pack()
    buttonKL = Button(fenetre, text="kitchen light", fg=color(kitchen.lightK), command= lambda: kitchen.kitchen("lightK",client,buttonKL))
    buttonKL.pack()
    buttonKH = Button(fenetre, text="kitchen hood", fg=color(kitchen.hood),command= lambda: kitchen.kitchen("hood",client,buttonKH))
    buttonKH.pack()
    buttonKC = Button(fenetre, text="kitchen cooker", fg=color(kitchen.cooker),command= lambda: kitchen.kitchen("cooker",client,buttonKC,buttonKH))
    buttonKC.pack()
    buttonKS = Button(fenetre, text="kitchen sink", fg=color(kitchen.sink),command= lambda: kitchen.kitchen("sink",client,buttonKS))
    buttonKS.pack()
    buttonBR1 = Button(fenetre, text="bedroom light1", fg=color(bedroom.lightR1),command= lambda: bedroom.bedroom("lightR1",client,buttonBR1))
    buttonBR1.pack()
    buttonBR2 = Button(fenetre, text="bedroom light2", fg=color(bedroom.lightR2),command= lambda: bedroom.bedroom("lightR2",client,buttonBR2))
    buttonBR2.pack()
    buttonBC = Button(fenetre, text="bedroom curtain", fg=color(bedroom.curtain),command= lambda: bedroom.bedroom("curtain",client,buttonODBC))
    buttonBC.pack()
    buttonBaL = Button(fenetre, text="bathroom light", fg=color(bathroom.lightB),command= lambda: bathroom.bathroom("lightB",client,buttonBaL))
    buttonBaL.pack()
    buttonBaS = Button(fenetre, text="bathroom shower", fg=color(bathroom.shower),command= lambda: bathroom.bathroom("shower",client,buttonBaS))
    buttonBaS.pack()
    buttonUL = Button(fenetre, text="utility_room light", fg=color(utility_room.lightU),command= lambda: utility_room.utility_room("lightU",client,buttonUL))
    buttonUL.pack()
    buttonUM = Button(fenetre, text="utility_room machine", fg=color(utility_room.machine),command= lambda: utility_room.utility_room("machine",client,buttonUM))
    buttonUM.pack()
    buttonOL = Button(fenetre, text="outside light", fg=color(outside.lightO),command= lambda: outside.outside("lightO",client,buttonOL))
    buttonOL.pack()
    buttonOI = Button(fenetre, text="outside lock", fg=color(outside.lock),command= lambda: outside.outside("lock",client,buttonOI))
    buttonOI.pack()
    buttonOD = Button(fenetre, text="outside door", fg=color(outside.door),command= lambda: outside.outside("door",client,buttonOD))
    buttonOD.pack()

    labelT= Label(fenetre, text="Set temperature: (Actual "+str(living_room.tempLimit)+")")
    labelT.pack()
    setTemp = Entry(fenetre)
    setTemp.pack()
    buttonT = Button(fenetre, text="Submit",command= lambda: living_room.temperature(setTemp.get(),client,labelT))
    buttonT.pack()
    global labelTAct
    labelTAct= Label(fenetre, text="temperature: ")
    labelTAct.pack()
    fenetre.mainloop()
    
def temp():
    global labelTAct
    try:
        while True:
            time.sleep(5)
            labelTAct["text"] = "temperature: "+str(client.get("living_room").payload)
    except KeyboardInterrupt:
        client.stop()
if __name__ == "__main__":
    threads = []
    try:
        for func in [GUI,temp]:
           threads.append(Thread(target=func))
           threads[-1].start()

        for thread in threads:
           """
           Waits for threads to complete before moving on with the main
           script.
           """
           thread.join()
    except:
        for thread in threads:
            thread.stop()