from threading import Lock, Thread
import time


def useTV(state):
   if state:
      print("TV on")
   else:
      print("TV off")

def useFan(state):
   if state:
      print("Fan on")
   else:
      print("Fan off")

def useLight(state):
   if state:
      print("Lights on")
   else:
      print("Lights off")

def useSink(state):
   if state:
      print("Sink on")
   else:
      print("Sink off")

def getTemperature():
    while True:
      print ("Temp is here")
      temp = 24
      if temp >= 25:
         useFan(True)
      else:
         useFan(False)
      time.sleep(1)
