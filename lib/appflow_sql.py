"""
Appflow SQL utilities.
This contains all the functions needed to perform SQL actions.
"""
import os

from flask_sqlalchemy import SQLAlchemy, declarative_base
from sqlalchemy import (Column, ForeignKey, Integer, String, Table,
                        create_engine)
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

from appflow_rest import app

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL') or 'sqlite:////tmp/app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
DB = SQLAlchemy(app)
DB_ENGINE = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)

DB_SESSION = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=DB_ENGINE))

BASE = declarative_base()
BASE.query = DB_SESSION.query_property()


def init_db():
    """
    Initialize DB
    This function will setup the tables and objects for the database
    """
    DB.init_app(app)
    BASE.metadata.create_all(bind=DB_ENGINE)


ASSOCIATION_TABLE = Table('association', BASE.metadata,
                          Column('username', Integer,
                                 ForeignKey('users.username')),
                          Column('tenantname', Integer,
                                 ForeignKey('tenants.name')))


class User(BASE):
    """
    User:
    this class represents the User entity. Contains generic data regardin the
    user and his credentials to access his own tenant.

    Auth methods include api-key (different for each associated tenant) and
    classic password auth (only on associated thenants.).
    """
    __tablename__ = 'users'
    username = Column(String(80), primary_key=True)
    mail = Column(String(80))
    password = Column(String(80))
    salt = Column(String(80), unique=True)
    username_recover = Column(String(80))
    mail_recover = Column(String(80))

    api_key = relationship("Api_key")
    tenants = relationship(
        "Tenant",
        secondary=ASSOCIATION_TABLE,
        back_populates="users")

    def __init__(self, username, mail, password, salt,
                 username_recover, mail_recover):
        self.username = username
        self.mail = mail
        self.password = password
        self.salt = salt
        self.username_recover = username_recover
        self.mail_recover = mail_recover

    def __repr__(self):
        return '<User %r>' % (self.username)


class Tenant(BASE):
    """
    Tenant:
    this class represents the Tenant entity. Contains data regarding the
    tenant and it's associated with multiple users.

    Only associated users can access this tenant
    via his API_KEY or authentication.
    """
    __tablename__ = 'tenants'
    name = Column(String(80), primary_key=True)
    secret = Column(String(80))
    name_recover = Column(String(80))

    api_key = relationship("Api_key")
    users = relationship(
        "User",
        secondary=ASSOCIATION_TABLE,
        back_populates="tenants")

    def __init__(self, name, secret, name_recover):
        self.name = name
        self.secret = secret
        self.name_recover = name_recover

    def __repr__(self):
        return '<Tenant %r>' % (self.name)


class ApiKey(BASE):
    """
    ApiKey:
    this class represents the ApiKey entity. Contains a unique
    link between each one user with his tenant.
    A key can correspond only to a single user-tenant association.
    """
    __tablename__ = 'api_key'
    key = Column(String(80), primary_key=True, unique=True)
    quota = Column(Integer)
    key_recover = Column(String(80))

    username = Column(String(80), ForeignKey('users.username'))
    tenantname = Column(String(80), ForeignKey('tenants.name'))

    user = relationship("User", back_populates="api_key")
    tenant = relationship("Tenant", back_populates="api_key")

    def __init__(self, key, quota, key_recover, user, tenant):
        self.key = key
        self.quota = quota
        self.key_recover = key_recover
        self.user = user
        self.tenant = tenant

    def __repr__(self):
        return '<Api_Key %r>' % (self.key)
