from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime
bcrypt = Bcrypt()
db = SQLAlchemy()

default_image = '/static/images/profile_pics/default_image.png'


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    username = db.Column(db.String(20),
                         nullable=False,
                         unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.Text, nullable=False,
                          default=default_image)
    searches = db.Relationship(
        'Search', backref='user')

    @classmethod
    def register(cls, first_name, last_name, email, username, password):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return True
        else:
            return False


class Phone(db.Model):
    __tablename__ = "phones"
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    number = db.Column(db.Text, nullable=False)
    valid = db.Column(db.Text, nullable=False)
    prefix = db.Column(db.Text, nullable=False)
    local = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    phone_type = db.Column(db.Text, nullable=False)
    carrier = db.Column(db.Text, nullable=False)


class Email(db.Model):
    __tablename__ = "emails"
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    email = db.Column(db.Text, nullable=False)
    is_valid = db.Column(db.Text, nullable=False)
    is_free_email = db.Column(db.Text, nullable=False)
    is_disposable = db.Column(db.Text, nullable=False)
    is_role = db.Column(db.Text, nullable=False)
    is_catchall = db.Column(db.Text, nullable=False)
    is_mx_found = db.Column(db.Text, nullable=False)
    is_smtp_valid = db.Column(db.Text, nullable=False)


class Vat (db.Model):
    __tablename__ = "vats"
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    number = db.Column(db.Text, nullable=False)
    valid = db.Column(db.Text, nullable=False)
    company_name = db.Column(db.Text, nullable=False)
    company_address = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)


class Domain(db.Model):
    __tablename__ = "domains"
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    domain = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    year_founded = db.Column(db.Text, nullable=False)
    industry = db.Column(db.Text, nullable=False)
    employees_count = db.Column(db.Text, nullable=False)
    locality = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    linkedin = db.Column(db.Text, nullable=False)


class Search(db.Model):
    __tablename__ = 'searches'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
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


def get_phone_pair(dict):
    for item in dict.items():
        country = Country(country_name=item[0], country_code=item[1])
        db.session.add(country)
        db.session.commit()


def get_vat_pair(dict):
    for item in dict.items():
        country = Vat_Country(country_name=item[1], country_code=item[0])
        db.session.add(country)
        db.session.commit()
