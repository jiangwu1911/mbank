# coding: utf-8
from bottle import route, get, post, delete, request, response, hook, static_file, redirect
from sqlalchemy import desc
import config
import logging
import json
import time
from model import Website, Traffic

logger = logging.getLogger(config.APP_NAME)

def obj_array_to_json(results, name):
    items = []
    for item in results:
        items.append(item.to_dict())
    return {name: items}


def define_route(app):
    @app.route('/', method='GET')
    def index():
        logger.info("Get homepage.")
        return("Back server for big screen.")

    @app.route('/website', method='GET')
    def get_website(db):
        websites = db.query(Website)\
                   .order_by(desc(Website.bytes_total))
        return obj_array_to_json(websites, 'websites')

    @app.route('/traffic', method='GET')
    def get_traffic(db):
        range = int(request.query.get('range'))

        # 如果没传begin,end参数, end用当前时间, 显示5分钟的数据
        if range is None:
             range = 300

        begin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-range))
        end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        traffic = db.query(Traffic).filter(Traffic.dt>begin, Traffic.dt<end)\
                  .order_by(Traffic.dt)
        return obj_array_to_json(traffic, 'traffic')
            
