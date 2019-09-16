# coding: utf-8
from bottle import route, get, post, delete, request, response, hook, static_file, redirect
from sqlalchemy import desc, func
import config
import logging
import json
import time
from model import Website, Traffic, Threat, Sysinfo, HTTPClient, Protocol, Region
from model import HttpConnectionNumber, HttpResponseTime
from model import DbConnectionNumber, DbResponseTime

logger = logging.getLogger(config.APP_NAME)

def obj_array_to_json(results, name):
    items = []
    for item in results:
        items.append(item.to_dict())
    return {name: items}

def obj_to_json(result, name):
    return {name: result.to_dict()}

def get_range(request):
    range = request.query.get('range')

    # 如果没传begin,end参数, end用当前时间, 显示5分钟的数据
    if range is None:
         range = 300
    else:
         range = int(range)

    begin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-range))
    end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    return (begin,end)

def get_input(req, varname):
    value = req.forms.get(varname)
    if value == None:
        value = req.query.get(varname)
    return value

def define_route(app):
    @app.route('/', method='GET')
    def index():
        #logger.info("Get homepage.")
        return("Back server for big screen.")

    @app.route('/website', method='GET')
    def get_website(db):
        t = db.query(func.max(Website.tsearch).label("max_tsearch")).subquery('t') 
        websites = db.query(Website)\
                   .filter(Website.tsearch == t.c.max_tsearch)\
                   .order_by(desc(Website.bytes_total))
        return obj_array_to_json(websites, 'websites')

    @app.route('/protocol', method='GET')
    def get_protocol(db):
        t = db.query(func.max(Protocol.tsearch).label("max_tsearch")).subquery('t')
        protocols = db.query(Protocol)\
                   .filter(Protocol.tsearch == t.c.max_tsearch)\
                   .order_by(desc(Protocol.bytes))
        return obj_array_to_json(protocols, 'protocols')

    @app.route('/region', method='GET')
    def get_region(db):
        t = db.query(func.max(Region.tsearch).label("max_tsearch")).subquery('t')
        regions = db.query(Region)\
                   .filter(Region.tsearch == t.c.max_tsearch)\
                   .order_by(desc(Region.bytes))
        return obj_array_to_json(regions, 'regions')

    @app.route('/httpclient', method='GET')
    def get_httpclient(db):
        t = db.query(func.max(HTTPClient.tsearch).label("max_tsearch")).subquery('t')
        httpclients = db.query(HTTPClient)\
                   .filter(HTTPClient.tsearch == t.c.max_tsearch)\
                   .order_by(desc(HTTPClient.bytes_total))
        return obj_array_to_json(httpclients, 'httpclients')

    @app.route('/traffic', method='GET')
    def get_traffic(db):
        (begin, end) = get_range(request)
        traffic = db.query(Traffic)\
                  .filter(Traffic.dt>begin, Traffic.dt<end)\
                  .order_by(Traffic.dt)
        return obj_array_to_json(traffic, 'traffic')
            
    @app.route('/http_connection_number', method='GET')
    def get_http_conns(db):
        (begin, end) = get_range(request)
        data = db.query(HttpConnectionNumber)\
               .filter(HttpConnectionNumber.dt>begin, HttpConnectionNumber.dt<end)\
               .order_by(HttpConnectionNumber.dt)
        return obj_array_to_json(data, 'http_connection_number')
            
    @app.route('/http_response_time', method='GET')
    def get_http_resp(db):
        (begin, end) = get_range(request)
        data = db.query(HttpResponseTime)\
               .filter(HttpResponseTime.dt>begin, HttpResponseTime.dt<end)\
               .order_by(HttpResponseTime.dt)
        return obj_array_to_json(data, 'http_response_time')
            
    @app.route('/db_connection_number', method='GET')
    def get_db_conns(db):
        (begin, end) = get_range(request)
        data = db.query(DbConnectionNumber)\
               .filter(DbConnectionNumber.dt>begin, DbConnectionNumber.dt<end)\
               .order_by(DbConnectionNumber.dt)
        return obj_array_to_json(data, 'db_connection_number')

    @app.route('/db_response_time', method='GET')
    def get_db_resp(db):
        (begin, end) = get_range(request)
        data = db.query(DbResponseTime)\
               .filter(DbResponseTime.dt>begin, DbResponseTime.dt<end)\
               .order_by(DbResponseTime.dt)
        return obj_array_to_json(data, 'db_response_time')

    @app.route('/threat', method='GET')
    def get_threat(db):
        threats = db.query(Threat)\
                   .order_by(Threat.no)
        return obj_array_to_json(threats, 'threats')

    @app.route('/sysinfo', method='GET')
    def get_sysinfo(db):
        sysinfo = db.query(Sysinfo).filter(Sysinfo.uptime>0)
        return obj_to_json(sysinfo[0], "sysinfo")

    @app.post('/alarm')
    def send_alarm(db):
        postdata = request.json
        message = postdata['result']['alarm_message']
        logger.info(message)

        import subprocess
        cmd = "/home/jwu/nt_bigscreen/sendsms.sh"
        output = subprocess.check_output([cmd, message])
        logger.info(output)
