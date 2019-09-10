# coding: utf-8
import time
import logging
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
import random

from model import Traffic, Sysinfo
import config

def create_db_engine():
    return create_engine('mysql://%s:%s@%s/%s?charset=%s' %
                         (config.DB_USER,
                          config.DB_PASSWORD,
                          config.DB_HOST,
                          config.DB_NAME,
                          config.DB_CHARSET),
                          echo=False)

def generate_test_traffic_data(db):
    t = time.time()
    traffic = Traffic(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)),
                      random.randint(50, 100))
    db.add(traffic)
    db.commit()

def get_uptime():
    system_online_date = '2018-11-01 00:00:00'
    t = time.mktime(time.strptime(system_online_date, "%Y-%m-%d %H:%M:%S"))
    now = time.time()
    return int((now-t)/86400)

def generate_test_sysinfo_data(db):
    result = db.query(Sysinfo).filter(Sysinfo.id==1)
    sysinfo = result.first()
    sysinfo.uptime = get_uptime()
    sysinfo.pct_cpu = random.randint(40, 50)
    sysinfo.pct_memory =  random.randint(30, 70)
    sysinfo.pct_disk = 10
    sysinfo.total_event = 118
    sysinfo.handled_event = 75
    sysinfo.pending_event = 43
    sysinfo.score = 78
    sysinfo.total_server = 1526
    sysinfo.total_client = 1526
    sysinfo.total_system = 1612
    sysinfo.server_with_problem = 249
    sysinfo.client_with_problem = 1136
    sysinfo.system_with_problem = 1018
    db.add(sysinfo)
    db.commit()

def generate_test_data():
    engine = create_db_engine()
    Session = sessionmaker(engine)
    db = Session()

    while(1):
        #generate_test_traffic_data(db)
        generate_test_sysinfo_data(db)
        time.sleep(5)

    db.close()
