from flask import Flask, request, make_response, jsonify, render_template, url_for, redirect, session
from sqlalchemy.exc import IntegrityError
import bcrypt
from functools import wraps

from db import database
from file_parser import file_parser
from engine import engine
from auth.auth import Authentication


app = Flask(__name__, template_folder='../templates', static_folder='../static')


pars = "parser"
postgres = "database"
eng = "engine"
key = "vDRif,gr!99A""N8*~3NY#*AkihiXQ&"
DEFAULT_SESSION_COOKIE_NAME = "session_id"


def is_authenticated():
    return DEFAULT_SESSION_COOKIE_NAME in request.cookies and \
        request.cookies[DEFAULT_SESSION_COOKIE_NAME] == "123"


def custom_login_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('/'))

        session.is_authenticated = True
        return function(*args, **kwargs)
    return decorator


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
    eng = engine.Engine()


@app.route("/get_results", methods=["POST"])
#@custom_login_required
def get_results():
    file = request.files['file']
    number_of_results = request.form['number']

    bad_request(file, 'Missing file!')
    bad_request(number_of_results, 'Missing number of results!')

    text_to_check = pars.get_data(file)

    all_data_from_db = postgres.get_all_data()
    all_sentences = postgres.get_all_sentences(all_data_from_db)

    ids, calculation_result = eng.start(all_sentences, [text_to_check], number_of_results)
    prepared_results = postgres.result_to_dict(all_data_from_db)
    result = eng.prepare_results(ids, prepared_results, calculation_result)

    return make_response(jsonify(result), 200)


@app.route("/insert_data", methods=["POST"])
#@custom_login_required
def insert_data_into_db():
    file = request.files['file']
    bad_request(file, 'Missing file!')

    content = pars.get_data(file)
    name = file.filename

    postgres.insert_data_for_search(name, content)

    return make_response("OK", 200)


@app.route("/delete_data", methods=["DELETE"])
#@custom_login_required
def delete_data_from_db():
    postgres.delete_data()
    return make_response("OK", 200)


@app.route("/get_data", methods=["GET"])
#@custom_login_required
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

        #if (request.cookies.get())

        req = request.get_json()

        login = req.get("login")
        password = req.get("password")

        bad_request(login, 'Missing login!')
        bad_request(password, 'Missing password!')

        customer = postgres.get_user_by_login(login)

        if not customer:
            return 'User Not Found!', 404

        if bcrypt.checkpw(password.encode('utf-8'), customer.password.encode('utf8')):
            response = make_response("OK", 200)

            response.set_cookie(DEFAULT_SESSION_COOKIE_NAME,
                                value="123",
                                httponly=True)

            return response
        else:
            return make_response('Invalid Login Info!', 400)

    else:
        return make_response("JSON not found", 400)


@app.route("/")
def start_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/user")
def user_page():
    return render_template("user.html")


@app.route("/admin")
def admin_page():
    return render_template("admin.html")
