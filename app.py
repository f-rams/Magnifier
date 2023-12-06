from flask import Flask, request, render_template
from models import connect_db, Country, Vat_Country
from fetchAPI import fetchDomain, fetchEmail, fetchPhone, fetchVAT
import os


SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 300,
    'pool_pre_ping': True
}
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'VITÓRIA123'
connect_db(app)
app.app_context().push()


@app.route('/')
def homepage():
    countries = Country.query.all()
    vat_codes = Vat_Country.query.all()
    return render_template('index.html',  countries=countries, vats=vat_codes)


@app.route('/search', methods=['POST'])
def search():
    type = request.json.get('type').capitalize()
    if type == 'Phone':
        return fetchPhone(type)
    elif type == 'Email':
        return fetchEmail(type)

    elif type == 'Vat':
        return fetchVAT(type)

    elif type == 'Domain':
        return fetchDomain(type)
