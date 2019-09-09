from sqlalchemy import Column, Integer, Float, Sequence, String, Text, DateTime, Unicode, Index
from sqlalchemy.ext.declarative import declarative_base
import datetime
import config
import logging

logger = logging.getLogger(config.APP_NAME)
Base = declarative_base()

class JsonObj():
    def to_dict(self):
        obj_dict = self.__dict__
        d = {}
        for key, val in obj_dict.items():
             if not key.startswith("_"):
                if isinstance(val, datetime.datetime):
                    d[key] = val.isoformat()
                else:
                    d[key] = val
        return d

class Website(Base, JsonObj): 
    __tablename__ = "website"
    id =  Column(Integer, Sequence('seq_pk'), primary_key=True)
    tsearch = Column(Integer, default=0, nullable=False)
    name = Column(String(100), nullable=False)
    bytes_in = Column(Integer, default=0, nullable=False)
    bytes_out = Column(Integer, default=0, nullable=False)
    bytes_total = Column(Integer, default=0, nullable=False)
    __table_args__ = (Index('index01', 'tsearch'),)

    def __init__(self, tsearch=0, name='', bytes_in=0, bytes_out=0, bytes_total=0):
        self.tsearch = tsearch
        self.name = name
        self.bytes_in = bytes_in
        self.bytes_out = bytes_out
        self.bytes_total = bytes_total

    def __repr__(self):
        return("<Website(%d, '%s', %d, %d, %d)>" 
            % (self.tsearch, self.name, self.bytes_in, self.bytes_out, self.bytes_total))

class Traffic(Base, JsonObj):
    __tablename__ = "traffic"
    id =  Column(Integer, Sequence('seq_pk'), primary_key=True)
    dt = Column(String(100), nullable=False)
    bytes = Column(Float, default=0, nullable=False)

    def __init__(self, dt='', bytes=0):
        self.dt = dt
        self.bytes = bytes

    def __repr__(self):
        return("<Traffic('%s', %.2f)>"
            % (self.dt, self.bytes))

class Threat(Base, JsonObj):
    __tablename__ = "threat"
    id = Column(Integer, Sequence('seq_pk'), primary_key=True)
    ip = Column(String(50), nullable=False)
    no = Column(Integer, nullable=False)
    server_group = Column(String(50), nullable=False)
    threat = Column(String(500), nullable=False)
    serverity = Column(String(100), nullable=False)

    def __init__(self, ip='', no=0, server_group='', threat='', serverity=''):
        self.ip = ip
        self.no = no
        self.server_group = server_group
        self.threat = threat
        self.serverity = serverity 

    def __repr__(self):
        return("<Threat('%s', %d, '%s', '%s', '%s')"
            % (self.ip, self.no, self.server_group, self.threat, self.serverity))

class Sysinfo(Base, JsonObj):
    __tablename__ = "sysinfo"
    id = Column(Integer, Sequence('seq_pk'), primary_key=True)
    uptime = Column(Integer, nullable=False)
    pct_cpu = Column(Integer, nullable=False)
    pct_memory = Column(Integer, nullable=False)
    pct_disk = Column(Integer, nullable=False)
    total_event = Column(Integer, nullable=False)
    handled_event = Column(Integer, nullable=False)
    pending_event = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    total_server = Column(Integer, nullable=False)
    total_client = Column(Integer, nullable=False)
    total_system = Column(Integer, nullable=False)
    server_with_problem = Column(Integer, nullable=False)
    client_with_problem = Column(Integer, nullable=False)
    system_with_problem = Column(Integer, nullable=False)

    def __init__(self, uptime=0, pct_cpu=0, pct_memory=0, pct_disk=0, total_event=0,
                 handled_event=0, pending_event=0, score=0, total_server=0, total_client=0,
                 total_system=0, server_with_problem=0, client_with_problem=0, system_with_problem=0):
        self.uptime = uptime
        self.pct_cpu = pct_cpu
        self.pct_memory = pct_memory
        self.pct_disk = pct_disk
        self.total_event = total_event
        self.handled_event = handled_event
        self.pending_event = pending_event
        self.score = score
        self.total_server = total_server
        self.total_client = total_client
        self.total_system = total_system
        self.server_with_problem = server_with_problem
        self.client_with_problem = client_with_problem
        self.system_with_problem = system_with_problem

    def __repr__(self):
        return("<Threat(%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)"
            % (self.uptime, self.pct_cpu, self.pct_memory, self.pct_disk, self.total_event,
               self.handled_event, self.pending_event, self.score, self.total_server, self.total_client, 
               self.total_system, self.server_with_problem, self.client_with_problem, self.system_with_problem))
