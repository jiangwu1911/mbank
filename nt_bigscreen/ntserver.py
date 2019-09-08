from bottle import route, run, request, Bottle
from paste import httpserver
import time
import socket
import json
import threading
import os
import signal
import sys
import logging

VERSION = "0.1"
APP_NAME = "ntserver"

app = Bottle()

logger = logging.getLogger(APP_NAME)

def init_log(logger):
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(APP_NAME+".log")
    console_handler = logging.StreamHandler()
    file_handler.setFormatter(fmt)
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

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

@app.route('/', method='GET')
def index():
    return("Back server for big screen.")

if __name__ == "__main__":
    init_log(logger)
    Watcher()
    logger.info("Server started")
    httpserver.serve(app, host="0.0.0.0", port=8080, threadpool_workers=30, request_queue_size=20)
