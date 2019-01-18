from threading import Thread
import RPi.GPIO as GPIO
import time
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from str2bool import str2bool
import json
import ast

LED = 9
lightO = False
ALARM = 11
alarm = False
DOOR = 26
door = False #state of the door
TRIG = 5
ECHO = 6
isOpen = False #locked or unlocked
doorOpen = False #open by the user?
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)
GPIO.setup(ALARM, GPIO.OUT)
GPIO.output(ALARM, GPIO.LOW)
GPIO.setup(DOOR, GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

p = GPIO.PWM(DOOR, 50)
p.start(7.5) # initial position

try:
    class OutsideResources(Resource):
        def __init__(self, name="BasicResource", coap_server=None):
            super(OutsideResources, self).__init__(name, coap_server,visible=True,observable=True,allow_children=True)
            self.payload = "Resource Data"
        def render_GET(self, request):
            return self
        def render_PUT(self, request):
            self.payload = request.payload
            return self
        def render_POST(self, request):
            data = ast.literal_eval(request.payload)
            res = OutsideResources()
            res.location_query = request.uri_query
            if(data["object"] == "light" ):
                res.payload = useLight(str2bool(data["state"]))
            elif (data["object"] == "door"):
                res.payload = useDoor(str2bool(data["state"]))
            elif (data["object"] == "lock"):
                res.payload = lock(str2bool(data["state"]))
            else:
                res.payload = False
            return res
        def render_DELETE(self, request):
            return True
        
    def useLight(state):
        global lightO
        print("on?",lightO)
        if state:
            print("Light on")
            GPIO.output(LED, GPIO.LOW)
            lightO = True
        else:
            print("Light off")
            GPIO.output(LED, GPIO.LOW)
            lightO = False

    def useAlarm(state):
        if state:
            print("Alarm on")
            GPIO.output(ALARM, GPIO.HIGH)
            alarm = True
        else:
            print("Alarm off")
            GPIO.output(ALARM, GPIO.LOW)
            alarm = False

    def useDoor(state, sensor = None):
        global doorOpen
        if isOpen & state:
            print("door opened")
            p.ChangeDutyCycle(3)
            door = True
            if sensor is None : #disable the server to use the door itself
                doorOpen = True
        else:
            print("door closed")
            p.ChangeDutyCycle(7.5)
            door = False
            if sensor is None :
                doorOpen = False
        return True

    def lock(state):
        global isOpen
        isOpen = state
        print("Door: ",isOpen)
        return True

    def moving():
        global isOpen,doorOpen
        while True:
            GPIO.output(TRIG, True)
            time.sleep(1)
            GPIO.output(TRIG, False)
            pulse_start = 0
            pulse_end = 0
            while GPIO.input(ECHO)==0:
                pulse_start = time.time()
            while GPIO.input(ECHO)==1:
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            move = pulse_duration * 17150
            move = round(move, 2)
            if isOpen == True:
                if move <= 5 and not doorOpen:
                    useDoor(True,True)
                elif not doorOpen and move > 5:
                    useDoor(False,True)
            else:
                if move <= 5 :
                    useAlarm(True)
                else:
                    useAlarm(False)
    def stop():
        p.stop()
        GPIO.cleanup()
except KeyboardInterrupt:                
    p.stop()
    GPIO.cleanup()