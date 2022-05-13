from flask import Flask, request, make_response, jsonify, render_template
from sqlalchemy.exc import IntegrityError
import bcrypt

from db import database
from file_parser import file_parser
from engine import engine


app = Flask(__name__, template_folder='../templates', static_folder='../static')


pars = "parser"
postgres = "database"
eng = "engine"


def bad_request(element, message):
    if not element:
        return make_response(message, 400)


@app.before_first_request
def initialization():
    global postgres
    global pars
    global eng

    postgres = database.Database(app)
    pars = file_parser.Parser()
    # eng = engine.Engine()


@app.route("/get_results", methods=["POST"])
def get_results():
    if request.is_json:
        req = request.get_json()

        text_to_check = [req.get("sentence")]
        number_of_results = req.get("number")

        bad_request(text_to_check, 'Missing text to check!')
        bad_request(number_of_results, 'Missing number of results!')

        all_data_from_db = postgres.get_all_data()
        all_sentences = postgres.get_all_sentences(all_data_from_db)
        ids, calculation_result = eng.start(all_sentences, text_to_check, number_of_results)
        prepared_results = postgres.result_to_dict(all_data_from_db)
        name_of_file, res = eng.prepare_results(ids, prepared_results, calculation_result)

        response = {
            "name": name_of_file,
            "result": res
        }

        return make_response(jsonify(response), 200)
    else:
        return make_response("JSON not found", 400)


@app.route("/insert_data", methods=["POST"])
def insert_data_into_db():
    if request.is_json:
        req = request.get_json()
        url = [req.get("url")]
        bad_request(url, 'Missing url!')

        content, name = pars.get_data(url[0])
        postgres.insert_data_for_search(name, content)

        return make_response("OK", 200)

    else:
        return make_response("JSON not found", 400)


@app.route("/delete_data", methods=["DELETE"])
def delete_data_from_db():
    postgres.delete_data()
    return make_response("OK", 200)


@app.route("/get_data", methods=["GET"])
def get_data_from_db():
    all_data_from_db = postgres.get_all_data()
    list_to_return = postgres.result_to_dict(all_data_from_db)

    return make_response(jsonify(list_to_return), 200)


@app.route("/register", methods=["POST"])
def register():
    if request.is_json:
        req = request.get_json()

        name = req.get("name")
        login = req.get("login")
        password = req.get("password")

        bad_request(name, 'Missing user name!')
        bad_request(login, 'Missing login!')
        bad_request(password, 'Missing password!')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            postgres.add_user(name, login, hashed_password.decode('utf8'))
        except IntegrityError:
            postgres.rollback()
            return make_response("User Already Exists", 400)

        return make_response("OK", 200)

    else:
        return make_response("JSON not found", 400)


@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        req = request.get_json()

        login = req.get("login")
        password = req.get("password")

        bad_request(login, 'Missing login!')
        bad_request(password, 'Missing password!')

        customer = postgres.get_user_by_login(login)

        if not customer:
            return 'User Not Found!', 404

        if bcrypt.checkpw(password.encode('utf-8'), customer.password.encode('utf8')):
            return make_response("OK", 200)
        else:
            return make_response('Invalid Login Info!', 400)

    else:
        return make_response("JSON not found", 400)


@app.route("/test")
def index():
    return render_template("login.html")


@app.route("/test2")
def index2():
    return render_template("register.html")


@app.route("/test3")
def index3():
    return render_template("user.html")
