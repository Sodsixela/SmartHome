import time
import RPi.GPIO as GPIO
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from str2bool import str2bool
import json
import ast

LED1 = 4
lightR1 = False
LED2 = 17
lightR2 = False
curtain = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT)
GPIO.output(LED1, GPIO.LOW)
GPIO.setup(LED2, GPIO.OUT)
GPIO.output(LED2, GPIO.LOW)

class BedroomResources(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(BedroomResources, self).__init__(name, coap_server,visible=True,observable=True,allow_children=True)
        self.payload = "Resource Data"
    def render_GET(self, request):
        return self
    def render_PUT(self, request):
        self.payload = request.payload
        return self
    def render_POST(self, request):
        data = ast.literal_eval(request.payload)
        res = BedroomResources()
        res.location_query = request.uri_query
        if(data["object"] == "light1" ):
            res.payload = useLight1(str2bool(data["state"]))
        elif (data["object"] == "light2"):
            res.payload = useLight2(str2bool(data["state"]))
        else:
            res.payload = False 
        return res
    def render_DELETE(self, request):
        return True
    
def useLight1(state):
    global lightR1
    if state:
        print("Light on")
        GPIO.output(LED1, GPIO.HIGH)
        lightR1 = True
    else:
        print("Light off")
        GPIO.output(LED1, GPIO.LOW)
        lightR1 = False
    return True
def useLight2(state):
    global R2
    if state:
        print("Light on")
        GPIO.output(LED2, GPIO.HIGH)
        lightR2 = True
    else:
        print("Light off")
        GPIO.output(LED2, GPIO.LOW)
        lightR2 = False
    return True

def stop():
    GPIO.cleanup()
