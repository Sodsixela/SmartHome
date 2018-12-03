from coapthon.client.helperclient import HelperClient
from tools import color

lightU = ""
machine = ""

def utility_room(object,client,button):
    path = "utility_room"
    if object == "machine":
        global machine
        machine = not machine
        response = client.post(path, {"object": object, "state": str(machine)})
        button["fg"]=color(machine)
    elif object == "lightU":
        global lightU
        lightU = not lightU
        response = client.post(path, {"object": "light", "state": str(lightU)})
        button["fg"]=color(lightU)