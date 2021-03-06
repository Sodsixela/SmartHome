from threading import Thread
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
import kitchen
from kitchen import KitchenResources
import living_room
from living_room import LivingRoomResources,temperature,bayState
import bathroom
from bathroom import BathroomResources
import bedroom
from bedroom import BedroomResources
import utility_room
from utility_room import UtilityRoomResources
import outside
from outside import OutsideResources,moving,doorState
import time
import sys

server =""
class Resources(Resource):
    def __init__(self, name="Resources", coap_server=None):
        super(Resources, self).__init__(name, coap_server,visible=True,observable=True,allow_children=True)
        self.payload = "{'lightO':"+ str(outside.lightO) +", 'door':"+str(outside.door) +", 'lock': " + str(outside.isOpen)
        self.payload = self.payload +", 'lightB':"+ str(bathroom.lightB) +", 'shower': "+str(bathroom.shower)
        self.payload = self.payload +", 'lightR1': "+ str(bedroom.lightR1)+", 'lightR2': "+ str(bedroom.lightR2)
        self.payload = self.payload +", 'lightK': "+str(kitchen.lightK)+", 'hood': "+str(kitchen.hood)+", 'cooker': "+str(kitchen.cooker)+", 'sink': "+str(kitchen.sink)
        self.payload = self.payload +", 'lightL': "+str(living_room.lightL)+",'tv': "+str(living_room.tv)+", 'fan': "+str(living_room.fan)+", 'tempLimit': "+str(living_room.tempLimit)+", 'bayWindow' :"+str(living_room.bayWindow)
        self.payload = self.payload +", 'lightU': "+str(utility_room.lightU)+", 'machine': "+str(utility_room.machine)+"}"
    def render_GET(self, request):
        return self
    def render_PUT(self, request):
        self.payload = "{'lightO':"+ str(outside.lightO) +", 'door':"+str(outside.door)+", 'lock': " + str(outside.isOpen)
        self.payload = self.payload +", 'lightB':"+ str(bathroom.lightB) +", 'shower': "+str(bathroom.shower)
        self.payload = self.payload +", 'lightR1': "+ str(bedroom.lightR1)+", 'lightR2': "+ str(bedroom.lightR2)
        self.payload = self.payload +", 'lightK': "+str(kitchen.lightK)+", 'hood': "+str(kitchen.hood)+", 'cooker': "+str(kitchen.cooker)+", 'sink': "+str(kitchen.sink)
        self.payload = self.payload +", 'lightL': "+str(living_room.lightL)+",'tv': "+str(living_room.tv)+", 'fan': "+str(living_room.fan)+", 'tempLimit': "+str(living_room.tempLimit)+", 'bayWindow' :"+str(living_room.bayWindow)
        self.payload = self.payload +", 'lightU': "+str(utility_room.lightU)+", 'machine': "+str(utility_room.machine)+"}"
        return self
    def render_POST(self, request):
        res = Resources()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res
    def render_DELETE(self, request):
        return True

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource("resources/", Resources())
        self.add_resource("living_room/", LivingRoomResources())
        self.add_resource("kitchen/", KitchenResources())
        self.add_resource("bedroom/", BedroomResources())
        self.add_resource("utility_room/", UtilityRoomResources())
        self.add_resource("bathroom/", BathroomResources())
        self.add_resource("outside/", OutsideResources())
        
def main():
    host = "0.0.0.0"
    port = 3005
    server = CoAPServer(host, port)
    server.listen(10)
    
if __name__ == '__main__':
    try:
        t_moving = Thread(target=moving)
        t_moving.daemon= True
        t_moving.start()
        
        t_temperature = Thread(target=temperature)
        t_temperature.daemon= True
        t_temperature.start()

        t_outsideDoor = Thread(target=doorState)
        t_outsideDoor.daemon = True
        t_outsideDoor.start()

        t_bay = Thread(target=bayState)
        t_bay.daemon = True
        t_bay.start()
        
        t_main = Thread(target=main)
        t_main.daemon= True
        t_main.start()
        while True:
            time.sleep(1)
    except (KeyboardInterrupt,SystemExit):
        print "Server Shutdown"
        if server != "":
            server.close()
        print "Exiting..."
        living_room.stop()
        #outside.stop()
        bathroom.stop()
        bedroom.stop()
        kitchen.stop()
        utility_room.stop()
        sys.exit()
