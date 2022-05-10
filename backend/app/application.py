from flask import Flask, request, make_response, jsonify

from db import database
from file_parser import file_parser
from engine import engine


app = Flask(__name__)

pars = "parser"
db = "database"
eng = "engine"


def bad_request(element, message):
    if not element:
        return make_response(message, 400)


@app.before_first_request
def initialization():
    global pars
    global db
    global eng

    pars = file_parser.Parser()
    db = database.Database()
    # eng = engine.Engine()


@app.route("/get_results", methods=["POST"])
def get_results():
    if request.is_json:
        req = request.get_json()

        text_to_check = [req.get("sentence")]
        number_of_results = req.get("number")

        bad_request(text_to_check, 'Missing text to check!')
        bad_request(number_of_results, 'Missing number of results!')

        all_data_from_db = db.get_all_data()
        all_sentences = db.get_all_sentences(all_data_from_db)
        ids, calculation_result = eng.start(all_sentences, text_to_check, number_of_results)
        name_of_file, res = eng.prepare_results(ids, all_data_from_db, calculation_result)

        response = {
            "name": name_of_file,
            "result": res
        }

        resp = make_response(jsonify(response), 200)
        return resp
    else:
        resp = make_response("JSON not found", 400)
        return resp


@app.route("/insert_data", methods=["POST"])
def insert_data_into_db():
    if request.is_json:
        req = request.get_json()

        url = [req.get("url")]

        bad_request(url, 'Missing url!')

        content, name = pars.get_data(url[0])
        db.insert_data_for_search(name, content)
        resp = make_response("OK", 200)
        return resp

    else:
        resp = make_response("JSON not found", 400)
        return resp


@app.route("/get_data", methods=["GET"])
def get_data_from_db():
    all_data_from_db = db.get_all_data()

    response = {
        "data": all_data_from_db
    }

    resp = make_response(jsonify(response), 200)
    return resp


@app.route("/delete_data", methods=["DELETE"])
def delete_data_from_db():
    db.delete_data()
    resp = make_response("OK", 200)
    return resp


@app.route("/registration", methods=["POST"])
def user_registration():
    if request.is_json:
        req = request.get_json()

        name = req.get("name")
        login = req.get("login")
        password = req.get("password")

        bad_request(name, 'Missing user name!')
        bad_request(login, 'Missing login!')
        bad_request(password, 'Missing password!')

        db.add_user(name, login, password)
        resp = make_response("OK", 200)
        return resp

    else:
        resp = make_response("JSON not found", 400)
        return resp
