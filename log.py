from flask import Flask, request, jsonify, render_template
from logging.handlers import RotatingFileHandler
from time import strftime
import logging
import traceback
from app import *



@app.route('/')

@app.after_request
def after_request(response):
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s',
                      ts,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  tb)
    return "Internal Server Error", 500

if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)
    logger.addHandler(handler)
    app.run()
