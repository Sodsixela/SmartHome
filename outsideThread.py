from threading import Thread
import time

isOpen = False

def useLight(state):
    if state:
      print("Light on")
    else:
      print("Light off")

def alarm(state):
    if state:
      print("Alarm on")
      time.sleep(1)
    else:
      print("Alarm off")

def useDoor(state):
    if isOpen & state:
      print("door opened")
    else:
      print("door closed")
      
def door(state):
    global isOpen
    isOpen = state
       
def moving():
    while True:
        move = True
        if isOpen == True:
            if move == True:
                useDoor(True)
            else:
                useDoor(False)
        else:
            if move == True:
                alarm(True)
            else:
                alarm(False)
                
