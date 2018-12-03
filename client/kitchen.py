from coapthon.client.helperclient import HelperClient
from tools import color

lightK = ""
hood = ""
cooker = ""
sink = ""

def kitchen(object,client, button, buttonB = None):
    path = "kitchen"
    #object = raw_input("object: ")
    if object == "hood":
        global hood
        hood = not hood
        response = client.post(path, {"object": object, "state": str(hood)})
        button["fg"]=color(hood)
    elif object == "cooker":
        global cooker
        cooker = not cooker
        response = client.post(path, {"object": object, "state": str(cooker)})
        button["fg"]=color(cooker)
        global hood
        hood = not hood
        buttonB["fg"]=color(hood)
    elif object == "sink":
        global sink
        sink = not sink
        response = client.post(path, {"object": object, "state": str(sink)})
        button["fg"]=color(sink)
    elif object =="lightK":
        global lightK
        lightK = not lightK
        response = client.post(path, {"object": "light", "state": str(lightK)})
        button["fg"]=color(lightK)