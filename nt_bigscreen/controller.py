from bottle import route, get, post, delete, request, response, hook, static_file, redirect
import config
import logging
import json
from model import Website

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
        websites = db.query(Website)
        return obj_array_to_json(websites, 'websites')
