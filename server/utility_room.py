import time
import RPi.GPIO as GPIO
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from str2bool import str2bool
import json
import ast

LED = 10
lightU = False
MACHINE = 12
machine = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

class UtilityRoomResources(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(UtilityRoomResources, self).__init__(name, coap_server,visible=True,observable=True,allow_children=True)
        self.payload = "Resource Data"
    def render_GET(self, request):
        return self
    def render_PUT(self, request):
        self.payload = request.payload
        return self
    def render_POST(self, request):
        data = ast.literal_eval(request.payload)
        res = UtilityRoomResources()
        res.location_query = request.uri_query
        if(data["object"] == "light" ):
            res.payload = useLight(str2bool(data["state"]))
        elif (data["object"] == "machine"):
            res.payload = useMachine(str2bool(data["state"]))
        else:
            res.payload = False 
        return res
    def render_DELETE(self, request):
        return True
    
def useLight(state):
    global lightU
    if state:
        print("Light on")
        GPIO.output(LED, GPIO.HIGH)
        lightU = True
    else:
        print("Light off")
        GPIO.output(LED, GPIO.LOW)
        lightU = False
    return True
def useMachine(state):
    global machine
    if state:
        print("Machine on")
        machine = True
    else:
        print("Machine off")
        machine = False
    return True
