from coapthon.client.helperclient import HelperClient
from tools import color

lightB = ""
shower = ""

def bathroom(object,client,button):
    path = "bathroom"
    if object == "shower":
        global shower
        shower = not shower
        response = client.post(path, {"object": object, "state": str(shower)})
        button["fg"]=color(shower)
    elif object == "lightB":
        global lightB
        lightB = not lightB
        response = client.post(path, {"object": "light", "state": str(lightB)})
        button["fg"]=color(lightB)
