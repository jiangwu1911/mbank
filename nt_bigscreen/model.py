from sqlalchemy import Column, Integer, Sequence, String, Text, DateTime, Unicode
from sqlalchemy.ext.declarative import declarative_base

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
    ip = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    requests = Column(Integer, default=0, nullable=False)

    def __init__(self, ip='', name='', requests=0):
        self.ip = ip
        self.name = name
        self.requests = requests

    def __repr__(self):
        return("<Website(%s, '%s', '%s', %d)>" % (self.id, self.ip, self.name, self.requests))
