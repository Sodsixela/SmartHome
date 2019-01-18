import time
import RPi.GPIO as GPIO
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from str2bool import str2bool
import json
import ast

LED = 22
lightK = False
HOOD = 18
hood = False
COOKER = 23
cooker = False
SINK = 16
sink = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)
GPIO.setup(HOOD, GPIO.OUT)
GPIO.output(HOOD, GPIO.LOW)
GPIO.setup(COOKER, GPIO.OUT)
GPIO.output(COOKER, GPIO.LOW)

class KitchenResources(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(KitchenResources, self).__init__(name, coap_server,visible=True,observable=True,allow_children=True)
        self.payload = "Resource Data"
    def render_GET(self, request):
        return self
    def render_PUT(self, request):
        self.payload = request.payload
        return self
    def render_POST(self, request):
        data = ast.literal_eval(request.payload)
        res = KitchenResources()
        res.location_query = request.uri_query
        if(data["object"] == "light" ):
            res.payload = useLight(str2bool(data["state"]))
        elif (data["object"] == "hood"):
            res.payload = useHood(str2bool(data["state"]))
        elif (data["object"] == "cooker"):
            res.payload = useCooker(str2bool(data["state"]))
        elif (data["object"] == "sink"):
            res.payload = useSink(str2bool(data["state"]))
        else:
            res.payload = False  
        return res
    def render_DELETE(self, request):
        return True
    
def useLight(state):
    global lightK
    if state:
        print("Light on")
        GPIO.output(LED, GPIO.HIGH)
        lightK= True
    else:
        print("Light off")
        GPIO.output(LED, GPIO.LOW)
        lightK = False
    return True
def useHood(state):
    global hood
    if state:
        print("Hood on")
        GPIO.output(HOOD, GPIO.HIGH)
        hood = True
    else:
        print("Hood off")
        GPIO.output(HOOD, GPIO.LOW)
        hood = False
    return True

def useCooker(state):
    global cooker
    if state:
        print("Cooker on")
        GPIO.output(COOKER, GPIO.HIGH)
        time.sleep(0.5)
        cooker = True
        useHood(True)
    else:
        print("Cooker off")
        GPIO.output(COOKER, GPIO.LOW)
        time.sleep(0.5)
        cooker = False
        useHood(False)
    return True
def useSink(state):
    global sink
    if state:
        print("Sink on")
        sink = True
    else:
        print("Sink off")
        sink = False
    return True

def stop():
    GPIO.cleanup()