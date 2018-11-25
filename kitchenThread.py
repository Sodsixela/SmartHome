from threading import Thread
import time

def useLight(state):
    if state:
      print("Light on")
   else:
      print("Light off")

def hood(state):
    if state:
      print("Hood on")
   else:
      print("Hood off")

def useCooker(state):
    if state:
      print("Cooker on")
      hood(True)
   else:
      print("Cooker off")
      hood(False)
      
