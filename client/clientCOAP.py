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
import sys

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
kitchen.lightK = home['lightK']
kitchen.hood = home['hood']
kitchen.cooker = home['cooker']
kitchen.sink = home['sink']
living_room.bayWindow = home['bayWindow']
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
    filename = PhotoImage(file = "SmartHome3D.png")
    C = Canvas(fenetre, height =400, width = 1000)
    background_label = Label(fenetre, image = filename)
    background_label.place(x=30,y=0, width = 600, height = 400)
    
    label = Label(fenetre, text="Smart Home")
    label.pack()
    label.place(x = 10, y = 20)
    buttonLL = Button(fenetre, text="light", fg=color(living_room.lightL), command= lambda: living_room.living_room("lightL",client,buttonLL))
    buttonLL.pack()
    buttonLL.place(x = 10, y = 130)
    buttonLF = Button(fenetre, text="fan", fg=color(living_room.fan),command= lambda: living_room.living_room("fan",client,buttonLF))
    buttonLF.pack()
    buttonLF.place(x = 10, y = 250)
    buttonLT = Button(fenetre, text="tv", fg=color(living_room.tv),command= lambda: living_room.living_room("tv",client,buttonLT))
    buttonLT.pack()
    buttonLT.place(x = 10, y = 290)
    buttonLB = Button(fenetre, text="bayWindow", fg=color(living_room.bayWindow),command= lambda: living_room.living_room("bayWindow",client,buttonLB))
    buttonLB.pack()
    buttonLB.place(x = 10, y = 100)
    buttonKL = Button(fenetre, text="light", fg=color(kitchen.lightK), command= lambda: kitchen.kitchen("lightK",client,buttonKL))
    buttonKL.pack()
    buttonKL.place(x = 150, y = 55)
    buttonKH = Button(fenetre, text="hood", fg=color(kitchen.hood),command= lambda: kitchen.kitchen("hood",client,buttonKH))
    buttonKH.pack()
    buttonKH.place(x = 250, y = 55)
    buttonKC = Button(fenetre, text="cooker", fg=color(kitchen.cooker),command= lambda: kitchen.kitchen("cooker",client,buttonKC,buttonKH))
    buttonKC.pack()
    buttonKC.place(x = 250, y = 95)
    buttonKS = Button(fenetre, text="sink", fg=color(kitchen.sink),command= lambda: kitchen.kitchen("sink",client,buttonKS))
    buttonKS.pack()
    buttonKS.place(x = 150, y = 95)
    buttonBR1 = Button(fenetre, text="light1", fg=color(bedroom.lightR1),command= lambda: bedroom.bedroom("lightR1",client,buttonBR1))
    buttonBR1.pack()
    buttonBR1.place(x = 560, y = 150)
    buttonBR2 = Button(fenetre, text="light2", fg=color(bedroom.lightR2),command= lambda: bedroom.bedroom("lightR2",client,buttonBR2))
    buttonBR2.pack()
    buttonBR2.place(x = 560, y = 270)
    buttonBaL = Button(fenetre, text="light", fg=color(bathroom.lightB),command= lambda: bathroom.bathroom("lightB",client,buttonBaL))
    buttonBaL.pack()
    buttonBaL.place(x = 370, y = 55)
    buttonBaS = Button(fenetre, text="shower", fg=color(bathroom.shower),command= lambda: bathroom.bathroom("shower",client,buttonBaS))
    buttonBaS.pack()
    buttonBaS.place(x = 370, y = 95)
    buttonUL = Button(fenetre, text="light", fg=color(utility_room.lightU),command= lambda: utility_room.utility_room("lightU",client,buttonUL))
    buttonUL.pack()
    buttonUL.place(x = 340, y = 340)
    buttonUM = Button(fenetre, text="machine", fg=color(utility_room.machine),command= lambda: utility_room.utility_room("machine",client,buttonUM))
    buttonUM.pack()
    buttonUM.place(x = 340, y = 370)
    buttonOL = Button(fenetre, text="light", fg=color(outside.lightO),command= lambda: outside.outside("lightO",client,buttonOL))
    buttonOL.pack()
    buttonOL.place(x = 160, y = 340)
    buttonOI = Button(fenetre, text="lock", fg=color(outside.lock),command= lambda: outside.outside("lock",client,buttonOI))
    buttonOI.pack()
    buttonOI.place(x = 240, y = 340)
    buttonOD = Button(fenetre, text="door", fg=color(outside.door),command= lambda: outside.outside("door",client,buttonOD))
    buttonOD.pack()
    buttonOD.place(x = 240, y = 370)
    C.pack()
    labelT= Label(fenetre, text="Set temperature: (Actual "+str(living_room.tempLimit)+")")
    labelT.pack()
    labelT.place(x = 10, y = 400)
    setTemp = Entry(fenetre)
    setTemp.pack()
    setTemp.place(x = 10, y = 430)
    buttonT = Button(fenetre, text="Submit",command= lambda: living_room.temperature(setTemp.get(),client,labelT))
    buttonT.pack()
    buttonT.place(x = 10, y = 460)
    global labelTAct
    labelTAct= Label(fenetre, text="temperature: ")
    labelTAct.pack()
    labelTAct.place(x = 10, y = 490)
    fenetre.mainloop()
    
def temp():
    global labelTAct
    while True:
        time.sleep(5)
        labelTAct["text"] = "temperature: "+str(client.get("living_room").payload)
if __name__ == "__main__":
    try:
        t_gui = Thread(target=GUI)
        t_gui.daemon= True
        t_gui.start()
        t_temp= Thread(target=temp)
        t_temp.daemon= True
        t_temp.start()
        while True:
            time.sleep(1)
    except (KeyboardInterrupt,SystemExit):
        print "Exiting..."
        client.stop()
        sys.exit()