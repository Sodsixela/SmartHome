#lock_tut.py
from threading import Lock, Thread
import time
import kitchenThread
from kitchenThread import kitchen
import living_roomThread
from living_roomThread import living_room
import bathroomThread
from bathroomThread import bathroom
import bedroomThread
from bedroomThread import bedroom
import utility_roomThread
from utility_roomThread import utility_room

try:
    def choice():
        while True:
            time.sleep(5)
            value = int(input("What do you want to do: \n1-Kitchen on \n2-Kithcen off \n3-Living room one \n4-Living room off"))
            if value == 1:
                kitchenThread.lockK.acquire()
            elif value == 2:
                kitchenThread.lockK.release()
            elif value == 3:
                living_roomThread.isOpen = True
            elif value == 4:
                living_roomThread.isOpen= False
            
    threads = []
    for func in [choice,moving, getTempreature]:
       threads.append(Thread(target=func))
       threads[-1].start()

    for thread in threads:
       """
       Waits for threads to complete before moving on with the main
       script.
       """
       thread.join()
except :
    for thread in threads:
        thread.stop()
