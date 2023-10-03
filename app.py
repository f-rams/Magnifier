from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from io import BytesIO
from PIL import Image
import re
from models import db, connect_db, User, Phone, Vat, Email, Search, Country, Domain, Vat_Country, default_image
from flask_bcrypt import Bcrypt
from datetime import datetime
import requests
import base64
import os
from dotenv import load_dotenv
load_dotenv()


PHONE_KEY = os.getenv('PHONE_KEY')
EMAIL_KEY = os.getenv('EMAIL_KEY')
VAT_KEY = os.getenv('VAT_KEY')
DOMAIN_KEY = os.getenv('DOMAIN_KEY')
CONFIG_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

current = os.getcwd()
parent_path = Path(current).parent

default_image = '/static/images/profile_pics/default_image.png'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = CONFIG_KEY
connect_db(app)
app.app_context().push()


@app.route('/')
def homepage():
    if not session.get('username'):
        return render_template('index.html')
    else:
        username = session['username']
        return redirect(f'/magnifier/{username}')


@app.route('/magnifier/<username>')
def main(username):
    if session.get('username'):
        user = User.query.filter(User.username == username).first()
        countries = Country.query.all()
        vat_codes = Vat_Country.query.all()
        return render_template('main.html', user=user, countries=countries, vats=vat_codes)
    else:
        return redirect('/')


@app.route('/magnifier/register', methods=['POST'])
def new_user():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    username = request.json.get('username')
    email = request.json.get('email')
    pwd = request.json.get('pwd')
    user_email_list = [user.email for user in User.query.all()]
    user_username_list = [user.username for user in User.query.all()]
    if email in user_email_list:
        return jsonify(response='Email already registered')
    if username in user_username_list:
        return jsonify(response='Username already registered')
    else:
        new_user = User.register(first_name, last_name, email, username, pwd)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return jsonify(response='Successful registration')


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    pwd = request.json.get('password')
    user = User.authenticate(username, pwd)
    if user:
        session['username'] = username
        return jsonify(response='Successful login')
    else:
        return jsonify(response='Invalid user')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


@app.route('/magnifier/<username>/edit')
def user_info(username):
    if session.get('username'):
        user = User.query.filter(User.username == username).first()
        return render_template('user.html', user=user)
    else:
        return redirect('/')


@app.route('/<username>/edit', methods=['PATCH'])
def edit_profile(username):
    user = User.query.filter(User.username == username).first()
    user.username = request.json.get('newUsername', user.username)
    user.email = request.json.get('email', user.email)
    db.session.commit()
    session['username'] = user.username
    response = jsonify(username=user.username,
                       email=user.email)
    return response


@app.route('/<username>/delete')
def delete_user(username):
    user = User.query.filter(User.username == username).first()
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    return redirect('/')


@app.route('/<username>/picture', methods=['PATCH'])
def edit_picture(username):
    user = User.query.filter(User.username == username).first()
    user_image_url = user.image_url
    if f'{user_image_url}' != f'{default_image}':
        os.remove(f'{current}{user_image_url}')
    image_file_encoded = request.json.get('image')
    if image_file_encoded == '':
        user.image_url = default_image
    else:
        now = re.sub(' ', '_', str(datetime.now()))
        image_directory = f'/static/images/profile_pics/{username}({now}).jpeg'
        image_path = f'{current}{image_directory}'
        image_edited = re.sub('^data:image/.+;base64,', '', image_file_encoded)
        decoded_image = base64.b64decode(image_edited)
        saved_image = Image.open(BytesIO(decoded_image)).convert('RGB')
        final_image = saved_image.transpose(Image.Transpose.ROTATE_270)
        final_image.save(image_path)
        user.image_url = image_directory
    db.session.commit()
    response = jsonify(image=user.image_url)
    return response


@app.route('/<username>/search', methods=['POST'])
def search(username):
    user = User.query.filter(User.username == username).first()
    type = request.json.get('type').capitalize()
    if type == 'Phone':
        phone = request.json.get('phoneNumber')
        country = request.json.get('countryCode')
        phone_number_complete = country+phone
        phone_number_list = [item.prefix +
                             item.number for item in Phone.query.all()]
        if phone_number_complete in phone_number_list:
            new_phone_search = Phone.query.filter(
                Phone.number == phone).first()
            new_search = Search(user_id=user.id, search_type=type,
                                phone_search_id=new_phone_search.id)
            db.session.add(new_search)
            db.session.commit()
        else:
            response = requests.get(
                f'https://phonevalidation.abstractapi.com/v1/?api_key={PHONE_KEY}&phone={country}{phone}').json()
            if response['valid'] == False:
                return jsonify(type=False)
            else:
                new_phone_search = Phone(number=phone, prefix=response['country']['prefix'], local=response['format']['local'],
                                         country=response['country']['name'], location=response['location'], valid=str(response['valid']), phone_type=response['type'].capitalize(), carrier=response['carrier'])
                db.session.add(new_phone_search)
                db.session.commit()
                new_search = Search(user_id=user.id, search_type=type,
                                    phone_search_id=new_phone_search.id)
                db.session.add(new_search)
                db.session.commit()
        count = len(user.searches)
        return jsonify(type=type, date=new_search.showdate, phone_number=new_phone_search.number, prefix=new_phone_search.prefix, local=new_phone_search.local, country=new_phone_search.country, location=new_phone_search.location, phone_type=new_phone_search.phone_type, carrier=new_phone_search.carrier, count=str(count))

    elif type == 'Email':
        email_address = request.json.get('emailAddress')
        email_address_list = [item.email for item in Email.query.all()]
        if email_address in email_address_list:
            new_email_search = Email.query.filter(
                Email.email == email_address).first()
            new_search = Search(user_id=user.id, search_type=type,
                                email_search_id=new_email_search.id)
            db.session.add(new_search)
            db.session.commit()
        else:
            response = requests.get(
                f'https://emailvalidation.abstractapi.com/v1/?api_key={EMAIL_KEY}&email={email_address}').json()
            if response['deliverability'] != 'DELIVERABLE':
                return jsonify(type=False)
            else:
                new_email_search = Email(email=email_address, is_valid=response['is_valid_format']['text'].capitalize(
                ), is_free_email=response['is_free_email']['text'].capitalize(), is_disposable=response['is_disposable_email']['text'].capitalize(), is_role=response['is_disposable_email']['text'].capitalize(), is_catchall=response['is_disposable_email']['text'].capitalize(), is_mx_found=response['is_disposable_email']['text'].capitalize(), is_smtp_valid=response['is_disposable_email']['text'].capitalize())
                db.session.add(new_email_search)
                db.session.commit()
                new_search = Search(user_id=user.id, search_type=type,
                                    email_search_id=new_email_search.id)
                db.session.add(new_search)
                db.session.commit()
        count = len(user.searches)
        return jsonify(type=type, date=new_search.showdate, email=new_email_search.email, valid=new_email_search.is_valid, free_email=new_email_search.is_free_email, disposable=new_email_search.is_disposable, role=new_email_search.is_role, catchall=new_email_search.is_catchall, mx=new_email_search.is_mx_found, smtp=new_email_search.is_smtp_valid, count=str(count))

    elif type == 'Vat':
        vat_number = request.json.get('vatNumber')
        vat_code = request.json.get('countryVat')
        vat_query = vat_code+vat_number
        vat_numbers_list = [item.number for item in Vat.query.all()]
        if vat_query in vat_numbers_list:
            new_vat_search = Vat.query.filter(
                Vat.number == vat_query).first()
            new_search = Search(
                user_id=user.id, search_type=type, vat_search_id=new_vat_search.id)
            db.session.add(new_search)
            db.session.commit()
        else:
            response = requests.get(
                f'https://vat.abstractapi.com/v1/validate/?api_key={VAT_KEY}&vat_number={vat_query}').json()
            new_vat_search = Vat(number=vat_query, valid=str(response['valid']).capitalize(), company_name=response['company']['name'],
                                 company_address=response['company']['address'], country=response['country']['name'])
            db.session.add(new_vat_search)
            db.session.commit()
            new_search = Search(user_id=user.id, search_type=type,
                                vat_search_id=new_vat_search.id)
            db.session.add(new_search)
            db.session.commit()
        count = len(user.searches)
        return jsonify(type=type, date=new_search.showdate, vat_number=new_vat_search.number, valid=new_vat_search.valid, company_name=new_vat_search.company_name, company_address=new_vat_search.company_address, country=new_vat_search.country, count=str(count))

    elif type == 'Domain':
        domain_address = request.json.get('domainAddress')
        domains_list = [item.domain for item in Domain.query.all()]
        if domain_address in domains_list:
            new_domain_search = Domain.query.filter(
                Domain.domain == domain_address).first()
            new_search = Search(user_id=user.id, search_type=type,
                                domain_search_id=new_domain_search.id)
            db.session.add(new_search)
            db.session.commit()
        else:

            response = requests.get(
                f'https://companyenrichment.abstractapi.com/v1/?api_key={DOMAIN_KEY}&domain={domain_address}').json()
            new_domain_search = Domain(name=response['name'], country=response['country'], employees_count=str(
                response['employees_count']), domain=response['domain'], industry=response['industry'], locality=response['locality'], year_founded=str(response['year_founded']), linkedin=response['linkedin_url'])
            db.session.add(new_domain_search)
            db.session.commit()
            new_search = Search(user_id=user.id, search_type=type,
                                domain_search_id=new_domain_search.id)
            db.session.add(new_search)
            db.session.commit()
        count = len(user.searches)
        return jsonify(type=type, date=new_search.showdate, name=new_domain_search.name, country=new_domain_search.country, employees_count=new_domain_search.employees_count, domain=new_domain_search.domain, industry=new_domain_search.industry, locality=new_domain_search.locality, year_founded=new_domain_search.year_founded, linkedin=new_domain_search.linkedin)


@app.route('/<int:id>/delete', methods=['POST'])
def delete_search(id):
    username = request.json.get('username')
    user = User.query.filter(User.username == username).first()
    search = Search.query.get(id)
    db.session.delete(search)
    db.session.commit()
    count = len(user.searches)
    return jsonify(user=username,  count=str(count))
