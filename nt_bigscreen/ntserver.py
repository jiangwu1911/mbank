# coding: utf-8
import bottle
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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
import random

import config
import controller
import model
from model import Traffic

VERSION = "0.1"

app = Bottle()

logger = logging.getLogger(config.APP_NAME)

def init_log(logger):
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(config.APP_NAME+".log")
    console_handler = logging.StreamHandler()
    file_handler.setFormatter(fmt)
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

def create_db_engine():
    return create_engine('mysql://%s:%s@%s/%s?charset=%s' %
                         (config.DB_USER,
                          config.DB_PASSWORD,
                          config.DB_HOST,
                          config.DB_NAME,
                          config.DB_CHARSET),
                          echo=False)

def install_db_plugin(app):
    engine = create_db_engine()
    model.Base.metadata.create_all(engine)

    create_session = sessionmaker(bind=engine)
    plugin = SQLAlchemyPlugin(engine,
                              model.Base.metadata,
                              create=True,
                              commit=True,
                              create_session=create_session)
    app.install(plugin)


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


def generate_test_traffic_data():
    engine = create_db_engine()
    Session = sessionmaker(engine)
    db = Session()
    
    while(1):
        t = time.time()
        traffic = Traffic(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)), 
                          random.randint(50, 100))
        db.add(traffic)
        db.commit()
        time.sleep(5)

    db.close() 


if __name__ == "__main__":
    init_log(logger)
    Watcher()

    # 生成测试流量数据
    t = threading.Thread(target=generate_test_traffic_data)
    t.start()

    bottle.ERROR_PAGE_TEMPLATE = """{"error": {"message": "{{e.body}}", "code": "{{e._status_code}}"}}"""
    app = Bottle()
    install_db_plugin(app)
    controller.define_route(app)

    logger.info("Server started")
    httpserver.serve(app, host="0.0.0.0", port=8080, threadpool_workers=30, request_queue_size=20)
