import os
import psycopg2
from flask import Flask, Blueprint, jsonify
from .instance.config import environments
from .api.controllers.book_controller import books_controller
from .api.models.database import Database


def create_app(flask_env):
    # We will be using the config variable to determine the database
    app = Flask(__name__, instance_relative_config=True)
    # app_config is a dictionary with all the possible environments and with the config classes as values
    app.config.from_object(environments[flask_env])

    db_url = environments[flask_env].Database_Url
    # this is required because the model/DatabaseConnection need to know the path to establish the connection
    os.environ["RUNNING_DB_PATH"] = db_url

    print("\n\n\n", db_url, "\n\n\n")

    # here we register our controllers
    app.register_blueprint(books_controller)
    return app
