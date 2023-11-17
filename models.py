from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime
bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Phone(db.Model):
    __tablename__ = "phones"
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    number = db.Column(db.Text, nullable=True, default="no data")
    valid = db.Column(db.Text, nullable=True, default="no data")
    prefix = db.Column(db.Text, nullable=True, default="no data")
    local = db.Column(db.Text, nullable=True, default="no data")
    country = db.Column(db.Text, nullable=True, default="no data")
    location = db.Column(db.Text, nullable=True, default="no data")
    phone_type = db.Column(db.Text, nullable=True, default="no data")
    carrier = db.Column(db.Text, nullable=True, default="no data")


class Email(db.Model):
    __tablename__ = "emails"
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    email = db.Column(db.Text, nullable=True, default="no data")
    is_valid = db.Column(db.Text, nullable=True, default="no data")
    is_free_email = db.Column(db.Text, nullable=True, default="no data")
    is_disposable = db.Column(db.Text, nullable=True, default="no data")
    is_role = db.Column(db.Text, nullable=True, default="no data")
    is_catchall = db.Column(db.Text, nullable=True, default="no data")
    is_mx_found = db.Column(db.Text, nullable=True, default="no data")
    is_smtp_valid = db.Column(db.Text, nullable=True, default="no data")


class Vat (db.Model):
    __tablename__ = "vats"
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    number = db.Column(db.Text, nullable=True, default="no data")
    valid = db.Column(db.Text, nullable=True, default="no data")
    company_name = db.Column(db.Text, nullable=True, default="no data")
    company_address = db.Column(db.Text, nullable=True, default="no data")
    country = db.Column(db.Text, nullable=True, default="no data")


class Domain(db.Model):
    __tablename__ = "domains"
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    domain = db.Column(db.Text, nullable=True, default="no data")
    name = db.Column(db.Text, nullable=True, default="no data")
    year_founded = db.Column(db.Text, nullable=True, default="no data")
    industry = db.Column(db.Text, nullable=True, default="no data")
    employees_count = db.Column(db.Text, nullable=True, default="no data")
    locality = db.Column(db.Text, nullable=True, default="no data")
    country = db.Column(db.Text, nullable=True, default="no data")
    linkedin = db.Column(db.Text, nullable=True, default="no data")


class Search(db.Model):
    __tablename__ = 'searches'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    search_type = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    phone_search_id = db.Column(db.Integer, db.ForeignKey(
        'phones.id'), nullable=True)
    email_search_id = db.Column(db.Integer, db.ForeignKey(
        'emails.id'), nullable=True)
    vat_search_id = db.Column(db.Integer, db.ForeignKey(
        'vats.id'), nullable=True)
    domain_search_id = db.Column(db.Integer, db.ForeignKey(
        'domains.id'), nullable=True)
    phone_searches = db.Relationship('Phone', backref='search')
    email_searches = db.Relationship('Email', backref='search')
    vat_searches = db.Relationship('Vat', backref='search')
    domain_searches = db.Relationship('Domain', backref='search')

    @property
    def showdate(cls):
        return cls.created_at.strftime("%d/%m/%Y at %H:%M:%S")


class Country(db.Model):
    __tablename__ = "countries"
    country_name = db.Column(db.Text, primary_key=True, autoincrement=False)
    country_code = db.Column(db.Text, nullable=False)


class Vat_Country(db.Model):
    __tablename__ = "vat_countries"
    country_name = db.Column(db.Text, primary_key=True, autoincrement=False)
    country_code = db.Column(db.Text, nullable=False)
