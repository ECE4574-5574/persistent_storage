from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import logging
import threading
import time
import sys
import dateutil.parser
import mysqlinterface
import structures as ds
from structures import Device, User, Room, House
import json
import parser

class HATSPersistentStorageRequestHandler(BaseHTTPRequestHandler):

    #When responsding to a request, the server instantiates a DeviceHubRequestHandler
    #and calls one of these functions on it.
    
    def do_GET(self):
        try:
            if parser.validateGetRequest(self.path):
                queryType = self.path.strip('/').split('/')[0]
                if queryType == 'HD':
                    houseID = parser.getHouseID(self.path)
                    if not houseID:
                      self.send_response(400)
                    body = ds.DumpJsonList(self.server.sqldb.get_house_devices(houseID))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    body = ds.DumpJsonList(self.server.sqldb.get_house_devices(houseID))
                    self.wfile.write(body)
                elif queryType == 'RD':
                    houseID = parser.getHouseID(self.path)
                    roomID = parser.getRoomID(self.path)
                    if not houseID or not roomID:
                      self.send_response(400)
                    body = ds.DumpJsonList(self.server.sqldb.get_room_devices(houseID, roomID))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(body)
                elif queryType == 'HT':
                    houseID = parser.getHouseID(self.path)
                    deviceType = parser.getDeviceType(self.path)
                    if not houseID or not deviceType:
                      send_response(400)
                    body = ds.DumpJsonList(self.server.sqldb.get_house_devices(houseID, deviceType))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(body)
                elif queryType == 'RT':
                    houseID = parser.getHouseID(self.path)
                    roomID = parser.getRoomID(self.path)
                    deviceType = parser.getDeviceType(self.path)
                    if not houseID or not roomID or not deviceType:
                      send_response(400)
                    body = ds.DumpJsonList(self.server.sqldb.get_room_devices(houseID, roomID, deviceType))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(body)
                elif queryType == 'BH':
                    houseID = parser.getHouseID(self.path)
                    if not houseID:
                      send_response(400)
                    blob = self.server.sqldb.get_house_data(houseID)
                    if blob is None or blob == '':
                        self.send_response(404)
                        self.end_headers()
                    else:
                        body=json.dumps({'version': 0, 'blob': blob})
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(body)
                elif queryType == 'BU':
                    userID = parser.getUserID(self.path)
                    if not userID:
                      send_response(400)
                    blob = self.server.sqldb.get_user_data(userID)
                    if blob is None or blob == '':
                        self.send_response(404)
                        self.end_headers()
                    else:
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(blob)
                elif queryType == 'BR':
                    houseID = parser.getHouseID(self.path)
                    roomID = parser.getRoomID(self.path)
                    if not houseID or not roomID:
                      send_response(400)
                    blob = self.server.sqldb.get_room_data(userID,roomID)
                    if blob is None or blob == '':
                        self.send_response(404)
                        self.end_headers()
                    else:
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(blob)
                elif queryType == 'BD':
                    houseID = parser.getHouseID(self.path)
                    deviceID = parser.getDeviceID(self.path)
                    roomID = parser.getRoomID(self.path)
                    if not houseID or not deviceID or not roomID:
                      send_response(400)
                    blob = self.server.sqldb.get_device_data(userID,deviceID,roomID)
                    if blob is None or blob == '':
                        self.send_response(404)
                        self.end_headers()
                    else:
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(blob)
                elif queryType == 'DD':
                    houseID = parser.getHouseID(self.path)
                    roomID = parser.getRoomID(self.path)
                    deviceID = parser.getDeviceID(self.path)
                    if not houseID or not roomID or not deviceID:
                      send_response(400)
                    body = ds.DumpJsonList(self.server.sqldb.get_device_data(houseID,deviceID,roomID))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    body = ds.DumpJsonList(self.server.sqldb.get_device_data(houseID,deviceID,roomID))
                    self.wfile.write(body) 
                else:
                    self.stubResponseOK()
            else:
                self.stubResponseBadReq()
        except:
            #For any other uncaught internal error, respond HTTP 500:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()

    def do_POST(self):
        try:
            if parser.validatePostRequest(self.path):
              queryType = self.path.strip('/').split('/')[0]
              if queryType == 'D':
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                deviceType = parser.getDeviceType(self.path)
                if not houseID or not roomID or not deviceType:
                  self.send_response(400)
                length = int(self.headers.getheader('content-length', 0))
                data = self.rfile.read(length)
                newDevice = Device(houseID, deviceType, data, roomID)
                if roomID == 0:
                  self.server.sqldb.insert_house_device(newDevice)
                else:
                  self.server.sqldb.insert_room_device(newDevice)
                self.send_response(200)
              elif queryType == 'R':
                houseID = parser.getHouseID(self.path)
                if not houseID:
                  self.send_response(400)
                length = int(self.headers.getheader('content-length', 0))
                data = self.rfile.read(length)
                newRoom = Room(houseID, data)
                self.server.sqldb.insert_room(newRoom)
                self.send_response(200)
              elif queryType == 'H':
                length = int(self.headers.getheader('content-length', 0))
                data = self.rfile.read(length)
                newHouse = House(data)
                self.send_response(200)
              elif queryType == 'U':
                length = int(self.headers.getheader('content-length', 0))
                data = self.rfile.read(length)
                newUser = User(data)
                self.server.sqldb.insert_user(newUser)
                self.send_response(200)
            else:
              self.stubResponseBadReq()
        except:
          f = open("output.txt", 'w')      
          e = sys.exc_info()
          f.write(e)
          print e
          self.stubResponseInternalErr()

    def do_PATCH(self):
        try:
            if parser.validatePatchRequest(self.path):
                self.stubResponseOK()
            else:
                self.stubResponseBadReq()
        except:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()

    def do_DELETE(self):
        try:
            if parser.validateDeleteRequest(self.path):
                self.stubResponseOK()
            else:
                self.stubResponseBadReq()
        except:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()

    def stubResponseOK(self):
        self.send_response(200)
        self.end_headers()

    def stubResponseBadReq(self):
        self.send_response(400)
        self.end_headers()

    def stubResponseInternalErr(self):
        self.send_response(500)
        self.end_headers()

class HATSPersistentStorageServer(HTTPServer):

    def __init__(self, server_address, RequestHandlerClass):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.shouldStop = False
        self.timeout = 1
        self.sqldb = mysqlinterface.MySQLInterface('matthew', 'password', 'test2')

    def serve_forever (self):
        while not self.shouldStop:
            self.handle_request()

def runServer(server):
    server.serve_forever()

## Starts a server on a background thread.
#  @param server the server object to run.
#  @return the thread the server is running on.
#          Retain this reference because you should attempt to .join() it before exiting.
def serveInBackground(server):
    thread = threading.Thread(target=runServer, args =(server,))
    thread.start()
    return thread

if __name__ == "__main__":
    LISTEN_PORT = 8080
    server = HATSPersistentStorageServer(('',LISTEN_PORT), HATSPersistentStorageRequestHandler)
    serverThread = serveInBackground(server)
    try:
        while serverThread.isAlive():
            print 'Serving...'
            time.sleep(10)
            print 'Still serving...'
            time.sleep(10)
    except KeyboardInterrupt:
        print 'Attempting to stop server (timeout in 30s)...'
        server.shouldStop = True
        serverThread.join(30)
        if serverThread.isAlive():
            print 'WARNING: Failed to gracefully halt server.'

