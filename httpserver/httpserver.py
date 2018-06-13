from bottle import route, run, request, Bottle
from paste import httpserver
import time
import socket
import json
import threading
import os
import signal
import sys
from Queue import *

OUTPUT_FILE="./bsb_request.log"
SERVER_IP="192.168.206.226"
SERVER_PORT=5555

app = Bottle()

class Watcher():  
    def __init__(self):  
        self.child = os.fork()  
        if self.child == 0:  
            return  
        else:  
            self.watch()  
  
    def watch(self):  
        try:  
            os.wait()  
        except KeyboardInterrupt:  
            self.kill()  
        sys.exit()  
  
    def kill(self):  
        try:  
            os.kill(self.child, signal.SIGKILL)  
        except OSError:  
            pass  

def get_hostname():
    myname = socket.getfqdn(socket.gethostname())
    return myname

def get_ipaddress():
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr

def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - long(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp

def send_messages(q):
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (SERVER_IP, SERVER_PORT)
        try:
            sock.connect(server_address)
            print "Connected to server"
            while True:
                msg = q.get(True)
                sock.sendall(msg+"\n")
        except Exception as e:
            print "Socket error: %s" % str(e)
        finally:
            sock.close()

        time.sleep(3)


hostname = get_hostname()
ipaddress = get_ipaddress()
queue = Queue()

@app.route('/', method='POST')
def index():
    dt =  get_time_stamp()
    body = request._get_body_string()

    message = {}
    message['timestamp'] = get_time_stamp()
    message['hostname'] = hostname
    message['source'] = ipaddress
    message['message'] = body

    msg = json.dumps(message, ensure_ascii=False)
    queue.put(msg, True)

if __name__ == "__main__":
    Watcher()
    t = threading.Thread(target=send_messages, args=(queue,))
    t.start()
    queue.join()
    httpserver.serve(app, host="0.0.0.0", port=8080, threadpool_workers=30, request_queue_size=20)
