import os
from flask import Blueprint, make_response, request, jsonify, send_from_directory
from flask import current_app as app
from ..validations.stock_validation import StockForm, StocksForm, TickersForm
from ..models.stock import Stock
from ..utils.excel_to_db import build_data_from_excel
from ..utils.db_to_excel import build_excel_from_db
from typing import Any
from cron import ROOT_DIR
from loguru import logger
import threading

stock_controller = Blueprint("stocks", __name__, url_prefix='/stocks')


@stock_controller.route("/details", methods=['GET'])
def obtain_stocks() -> Any:
    try:
        records = Stock().extract_stocks()
        return make_response(jsonify({
            "error": False,
            "result": records
        }), 200)
    except Exception as error:
        print("ERROR ", error)
        return make_response(jsonify({
            "error": "obtaining the stock was unsuccessful",
            "message": "obtaining the stock was unsuccessful",
            "status": 400
        }), 400)

@stock_controller.route('/', methods=['GET'])
def get_stocks() -> Any:
    try:
        records = Stock().all()
        return jsonify({
            "error": False,
            "result": records}), 200
    except Exception as error:
        print("ERROR get_stocks> ", error)
        return jsonify({
            "error": "can't get list",
            "message": "can't get list",
        }), 400
