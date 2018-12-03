from threading import Lock, Thread
import time
import RPi.GPIO as GPIO
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from str2bool import str2bool
import json
import ast
import os
import glob

TV = 24
tv = False
FAN = 25
fan = False
fanOn = False # if the user put it on, the server cannot use it itself
LED = 20
lightL = False
TEMP = 13
tempLimit = 25
actTemp = 20 
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')
#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'


class LivingRoomResources(Resource):
    def __init__(self, name="LivingRoomResources", coap_server=None):
        super(LivingRoomResources, self).__init__(name, coap_server,visible=True,observable=True,allow_children=True)
        self.payload = str(actTemp)
        
    def render_GET(self, request):
        return self
    
    def render_PUT(self, request):
        data = ast.literal_eval(request.payload)
        global tempLimit
        tempLimit = data["object"]
        return self
    
    def render_POST(self, request):
        data = ast.literal_eval(request.payload)
        res = LivingRoomResources()
        res.location_query = request.uri_query
        if(data["object"] == "light" ):
            useLight(str2bool(data["state"]))
        elif (data["object"] == "fan"):
            useFan(str2bool(data["state"]))
        elif (data["object"] == "tv"):
            useTV(str2bool(data["state"]))
        elif (data["object"] == "temperature"):
            useTemperature(str2bool(data["state"]))
        return res
    
    def render_DELETE(self, request):
        return True
    
    
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def useTV(state):
    global tv
    if state:
        print("TV on")
        tv = True
    else:
        print("TV off")
        tv = False
    return True
def useFan(state, temp = None):
    global fan
    if state:
        print("Fan on")
        fan = True
        if temp is None:
            fanOn = True
    else:
        print("Fan off")
        fan = False
        if temp is None:
            fanOn = False
    return True
def useLight(state):
    global lightL
    if state:
        print("Lights on")
        GPIO.output(LED, GPIO.HIGH)
        lightL = True
    else:
        print("Lights off")
        GPIO.output(LED, GPIO.LOW)
        lightL = False
    return True

def temperature():
    global actTemp
    while True:
        #actTemp = read_temp()[0]
        if actTemp >= tempLimit and not fanOn:
            useFan(True,True)
        elif fan and not fanOn:
            useFan(False,True)
        time.sleep(1)
