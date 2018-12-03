from coapthon.client.helperclient import HelperClient
from tools import color

tv = ""
fan = ""
lightL = ""
tempLimit = ""
def temperature(object,client,labelT):
    path = "living_room"
    response = client.put(path, {"object": object})
    tempLimit = object
    labelT["text"]="Set temperature: (Actual "+str(tempLimit)+")"
    
def living_room(object,client,button):
    path = "living_room"
    #object = raw_input("object: ")
    if object == "tv":
        global tv
        tv = not tv
        response = client.post(path, {"object": object, "state": str(tv)})
        button["fg"]=color(tv)
    elif object == "fan":
        global fan
        fan = not fan
        response = client.post(path, {"object": object, "state": str(fan)})
        button["fg"]=color(fan)
    elif object =="lightL":
        global lightL
        lightL = not lightL
        response = client.post(path, {"object": "light", "state": str(lightL)})
        button["fg"]=color(lightL)