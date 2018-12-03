from coapthon.client.helperclient import HelperClient
from tools import color


lightO = ""
#alarm = home['alarm']
door = ""
lock = ""

def outside(object,client,button):
    path = "outside"
    #object = raw_input("object: ")
    if object == "lock":
        global lock
        lock = not lock
        response = client.post(path, {"object": object, "state": str(lock)})
        button["fg"]=color(lock)
    elif object == "door":
        global door
        door = not door
        response = client.post(path, {"object": object, "state": str(door)})
        button["fg"]=color(door)
    elif object =="lightO":
        global lightO
        lightO = not lightO
        response = client.post(path, {"object": "light", "state": str(lightO)})
        button["fg"]=color(lightO)