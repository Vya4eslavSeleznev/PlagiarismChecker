from datetime import timedelta
from functools import wraps
import re
import bcrypt
from flask import Flask, request, make_response, jsonify, render_template, url_for, redirect
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, current_user, unset_jwt_cookies, \
    JWTManager
from sqlalchemy.exc import IntegrityError

from db import database
from engine import engine
from file_parser import file_parser

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_ACCESS_COOKIE_NAME'] = 'session_id'

jwt = JWTManager(app)

pars = 'parser'
postgres = 'database'
eng = 'engine'
key = 'vDRif,gr!99A""N8*~3NY#*AkihiXQ&'
DEFAULT_SESSION_COOKIE_NAME = 'session_id'


def admin_only(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        if current_user is not None and current_user.admin:
            return function(*args, **kwargs)

        return redirect(url_for('start_page'))

    return decorator


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return postgres.get_user_by_login(identity)


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


def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


@app.route('/get_results', methods=['POST'])
@jwt_required()
def get_results():
    file = request.files['file']
    number_of_results = request.form['number']

    bad_request(file, 'Missing file!')
    bad_request(number_of_results, 'Missing number of results!')

    number_of_rows = postgres.count_rows()

    if number_of_rows == 0:
        return make_response(jsonify([]), 404)

    text_to_check = pars.get_data(file)

    if is_english(text_to_check):
        all_data_from_db = postgres.get_all_data()
        all_sentences = postgres.get_all_sentences(all_data_from_db)

        ids, calculation_result = eng.start(all_sentences, [text_to_check], number_of_results)
        prepared_results = postgres.result_to_dict(all_data_from_db)
        result = eng.prepare_results(ids, prepared_results, calculation_result)

        return make_response(jsonify(result), 200)

    return make_response('Check the file extension or data', 400)


@app.route('/insert_data', methods=['POST'])
@jwt_required()
def insert_data_into_db():
    file = request.files['file']
    bad_request(file, 'Missing file!')

    name = file.filename

    if name.endswith(('.doc', '.docx')):
        content = pars.get_data(file)
        postgres.insert_data_for_search(name, content)
        return make_response('OK', 200)

    return make_response('Check the file extension', 400)


@app.route('/delete_data', methods=['DELETE'])
@jwt_required()
def delete_data_from_db():
    postgres.delete_data()
    return make_response('OK', 200)


@app.route('/get_data', methods=['GET'])
@jwt_required()
def get_data_from_db():
    all_data_from_db = postgres.get_all_data()
    list_to_return = postgres.result_to_dict(all_data_from_db)

    return make_response(jsonify(list_to_return), 200)


@app.route('/register', methods=['POST'])
def register():
    if request.is_json:
        req = request.get_json()

        name = req.get('name')
        login = req.get('login')
        password = req.get('password')

        bad_request(name, 'Missing user name!')
        bad_request(login, 'Missing login!')
        bad_request(password, 'Missing password!')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            postgres.add_user(name, login, hashed_password.decode('utf8'))
        except IntegrityError:
            postgres.rollback()
            return make_response('User Already Exists', 400)

        return make_response('OK', 200)

    else:
        return make_response('JSON not found', 400)


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:

        # if (request.cookies.get())

        req = request.get_json()

        login = req.get('login')
        password = req.get('password')

        bad_request(login, 'Missing login!')
        bad_request(password, 'Missing password!')

        customer = postgres.get_user_by_login(login)

        if not customer:
            return 'User Not Found!', 404

        if bcrypt.checkpw(password.encode('utf-8'), customer.password.encode('utf8')):
            # response = make_response("OK", 200)
            # value_if_true if condition else value_if_false
            response = make_response(jsonify({"url": url_for('admin_page' if customer.admin else 'user_page')}), 200)

            access_token = create_access_token(identity=login)
            set_access_cookies(response, access_token)

            return response
        else:
            return make_response('Invalid Login Info!', 400)

    else:
        return make_response('JSON not found', 400)


@app.route('/logout', methods=['POST'])
def logout():
    response = make_response('OK', 200)
    unset_jwt_cookies(response)
    return response


@app.route('/')
def start_page():
    return render_template('login.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/user')
@jwt_required()
def user_page():
    test = current_user
    return render_template('user.html')


@app.route('/admin')
@jwt_required()
@admin_only
def admin_page():
    return render_template('admin.html')
