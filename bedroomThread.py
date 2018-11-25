from threading import Thread
import time

def useLight1(state):
    if state:
      print("Light on")
   else:
      print("Light off")

def useLight2(state):
    if state:
      print("Light on")
   else:
      print("Light off")

def curtain(state):
    if state:
      print("Curtain on")
   else:
      print("Curtain off")
