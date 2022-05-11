from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

from model import models
from db import config


class Database:

    def __init__(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = config.database_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.db = SQLAlchemy(app)
        self.engine = create_engine(config.database_uri)
        models.Base.metadata.create_all(self.engine)

    def insert_data_for_search(self, name, content):
        data = models.Data(name, content)
        self.db.session.add(data)
        self.db.session.commit()

    def delete_data(self):
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)

    def get_all_data(self):
        result = self.db.session.query(models.Data).all()
        return result

    def add_user(self, name, login, password):
        customer = models.Customer(name, login, password)
        self.db.session.add(customer)
        self.db.session.commit()

    @staticmethod
    def get_all_sentences(result_data):
        all_sentences = []

        for index, item in enumerate(result_data):
            all_sentences.append(item.content)

        return all_sentences

    @staticmethod
    def result_to_dict(all_data_from_db):
        list_to_return = []

        for index, item in enumerate(all_data_from_db):
            list_to_return.append(all_data_from_db[index].as_dict())

        return list_to_return
