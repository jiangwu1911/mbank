from bottle import route, get, post, delete, request, response, hook, static_file, redirect
import config
import logging

logger = logging.getLogger(config.APP_NAME)

def define_route(app):
    @app.route('/', method='GET')
    def index():
        logger.info("Get homepage.")
        return("Back server for big screen.")
