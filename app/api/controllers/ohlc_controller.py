from flask import Blueprint, make_response, request, jsonify, send_from_directory
from ..models.stock import OHLCData


ohlc_controller = Blueprint("ohlc", __name__, url_prefix='/ohlc')

@ohlc_controller.route('days_return')
def days_return(days=1):
    try:
        days = request.args.get('days', default = 1, type = int)
        response = OHLCData().days_return(days)
        for r in response:
            r['days_return'] = float(r['days_return'])

        return make_response(jsonify({'status': 'ok', "result": response}), 200)
    except Exception as error:
        print(error)
        return make_response(jsonify({
            "error": "obtaining days return was unsuccessful",
            "message": "obtaining days return was unsuccessful",
            "status": 400
        }), 400)