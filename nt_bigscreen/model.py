from sqlalchemy import Column, Integer, Float, Sequence, String, Text, DateTime, Unicode
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
    name = Column(String(100), nullable=False)
    bytes_in = Column(Integer, default=0, nullable=False)
    bytes_out = Column(Integer, default=0, nullable=False)
    bytes_total = Column(Integer, default=0, nullable=False)

    def __init__(self, name='', requests=0):
        self.name = name
        self.bytes_in = bytes_in
        self.bytes_out = bytes_out
        self.bytes_total = bytes_total

    def __repr__(self):
        return("<Website('%s', %d, %d, %d)>" 
            % (self.name, self.bytes_in, self.bytes_out, self.bytes_total))

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
 
  
