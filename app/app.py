from flask import Flask
from flask import request, jsonify
from .instance.config import environments
#from .api.controllers.book_controller import books_controller
#from .api.controllers.stock_controller import stock_controller
from .api.controllers.ohlc_controller import ohlc_controller
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)


def create_app(flask_env):
    # We will be using the config variable to determine the database
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    @app.before_request
    def check_header_for_authentication():
        # print("before_request is running!")

        # CORS SEND AN OPTION REQUEST BEFORE EVERY GET AND POST
        # WE NEED FILTER THESE REQUEST AND ALLOW A CORRECT RESPONSE
        if request.method == 'OPTIONS':
            return

    # Disable cache for download excel file
    @app.after_request
    def add_header(response):
        # response.cache_control.no_store = True
        if 'Cache-Control' not in response.headers:
            response.headers['Cache-Control'] = 'no-store'
        return response

    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['STOCKS_FILE_NAME'] = 'angkasa_excel.xlsx'

    app.config.from_object(environments[flask_env])
    
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#    app.register_blueprint(books_controller)
#    app.register_blueprint(stock_controller)
    app.register_blueprint(ohlc_controller)
    return app


"""
    @app.after_request  # blueprint can also be app~~
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3006'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Auth-Token'
        print("fixing CORS")

        if response.status_code is 308:
            response.status_code = 200

        return response
"""

# environments is a dictionary with all the possible environments and with the config classes as values
