from coapthon.client.helperclient import HelperClient
from tools import color


lightR1 = ""
lightR2 = ""

def bedroom(object,client,button):
    path = "bedroom"
    if object == "lightR1":
        global lightR1
        lightR1 = not lightR1
        response = client.post(path, {"object": "light1", "state": str(lightR1)})
        button["fg"]=color(lightR1)
    elif object =="lightR2":
        global lightR2
        lightR2 = not lightR2
        response = client.post(path, {"object": "light2", "state": str(lightR2)})
        button["fg"]=color(lightR2)