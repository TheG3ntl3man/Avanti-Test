from flask import Blueprint, request, jsonify, abort, make_response
from ..models.book import Book
from ..helpers import records_to_py

books_controller = Blueprint("books", __name__, url_prefix='/book')


@books_controller.route('/create', methods=['POST'])
def add_book():
    try:
        req = request.get_json()
        print(req)
        Book().insert(req['title'],
                      req['description'],
                      req['author'])

        return jsonify({
            "status": 201,
            "message": "book created successfully"
        }), 201

    except Exception:
        return jsonify({
            "error": "invalid book data input",
            "message": "missing or wrong parameters",
            "status": 400
        }), 400


@books_controller.route('/', methods=['GET'])
def get_books():
    try:
        records = Book().all()

        return jsonify({
            "result": records}), 200

    except Exception as error:
        print("ERROR get_books> ", error)
        return jsonify({
            "error": "can't get list",
            "message": "I was unable to retrieve the book list, please try again",
            "status": 400
        }), 400


@books_controller.route('/sample', methods=['GET'])
def sample():
    return jsonify({
        "result": "OK"}), 200
