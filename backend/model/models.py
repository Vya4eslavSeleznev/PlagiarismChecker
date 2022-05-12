from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, UniqueConstraint

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    login = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)

    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password

    def __repr__(self):
        return "<Customer(name='{}', login='{}', password={})>" \
            .format(self.name, self.login, self.password)


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    content = Column(Text, nullable=False)

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __repr__(self):
        return "<Data(name='{}', content='{}')>" \
            .format(self.name, self.content)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
