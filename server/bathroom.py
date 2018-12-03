import time
import RPi.GPIO as GPIO
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from str2bool import str2bool
import json
import ast

LED = 2
lightB = False
SHOWER = 3
shower = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

class BathroomResources(Resource):
    def __init__(self, name="BathroomResources", coap_server=None):
        super(BathroomResources, self).__init__(name, coap_server,visible=True,observable=True,allow_children=True)
    def render_GET(self, request):
        return self    
    def render_PUT(self, request):
        self.payload = request.payload
        return self
    def render_POST(self, request):
        print("request asked:  ",request.payload)
        data = ast.literal_eval(request.payload)
        print("data:,", data)
        res = BathroomResources()
        res.location_query = request.uri_query
        if(data["object"] == "light" ):
            res.payload = useLight(str2bool(data["state"]))
        elif (data["object"] == "shower"):
            res.payload = useShower(str2bool(data["state"]))
        else:
            res.payload = False    
        return res
    
    def render_DELETE(self, request):
        return True
    
def useLight(state):
    global lightB
    if state:
        print("Light on")
        GPIO.output(LED, GPIO.HIGH)
        lightB = True
    else:
        print("Light off")
        GPIO.output(LED, GPIO.LOW)
        lightB = False
    return True

def useShower(state):
    global shower
    if state:
        print("Shower on")
        shower = True
    else:
        print("Shower off")
        shower = False
    return True 
