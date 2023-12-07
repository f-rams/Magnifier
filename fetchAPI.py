from flask import request, jsonify
from models import db, Phone, Vat, Email, Search, Domain
import requests
import os


PHONE_KEY = os.getenv('PHONE_KEY')
EMAIL_KEY = os.getenv('EMAIL_KEY')
VAT_KEY = os.getenv('VAT_KEY')
DOMAIN_KEY = os.getenv('DOMAIN_KEY')


def fetchVAT(type):
    vat_number = request.json.get('vatNumber')
    vat_code = request.json.get('countryVat')
    vat_query = vat_code+vat_number
    vat_numbers_list = [item.number for item in Vat.query.all()]
    if vat_query in vat_numbers_list:
        new_vat_search = Vat.query.filter(Vat.number == vat_query).first()
        new_search = Search(search_type=type, vat_search_id=new_vat_search.id)
        db.session.add(new_search)
        db.session.commit()
        db.session.close()
    else:
        response = requests.get(
            f'https://vat.abstractapi.com/v1/validate/?api_key={VAT_KEY}&vat_number={vat_query}').json()
        new_vat_search = Vat(number=vat_query, valid=str(response['valid']).capitalize(), company_name=response['company']['name'],
                             company_address=response['company']['address'], country=response['country']['name'])
        db.session.add(new_vat_search)
        db.session.commit()
        new_search = Search(search_type=type,
                            vat_search_id=new_vat_search.id)
        db.session.add(new_search)
        db.session.commit()
        db.session.close()
    return jsonify(type=type, date=new_search.showdate, vat_number=new_vat_search.number, valid=new_vat_search.valid, company_name=new_vat_search.company_name, company_address=new_vat_search.company_address, country=new_vat_search.country)


def fetchDomain(type):
    domain_address = request.json.get('domainAddress')
    domains_list = [item.domain for item in Domain.query.all()]
    if domain_address in domains_list:
        new_domain_search = Domain.query.filter(
            Domain.domain == domain_address).first()
        new_search = Search(
            search_type=type, domain_search_id=new_domain_search.id)
        db.session.add(new_search)
        db.session.commit()
        db.session.close()
    else:
        response = requests.get(
            f'https://companyenrichment.abstractapi.com/v1/?api_key={DOMAIN_KEY}&domain={domain_address}').json()
        new_domain_search = Domain(name=response['name'], country=response['country'], employees_count=str(response['employees_count']), domain=response['domain'],
                                   industry=response['industry'], locality=response['locality'], year_founded=str(response['year_founded']), linkedin=response['linkedin_url'])
        db.session.add(new_domain_search)
        db.session.commit()
        new_search = Search(
            search_type=type, domain_search_id=new_domain_search.id)
        db.session.add(new_search)
        db.session.commit()
        db.session.close()
    return jsonify(type=type, date=new_search.showdate, name=new_domain_search.name, country=new_domain_search.country, employees_count=new_domain_search.employees_count, domain=new_domain_search.domain, industry=new_domain_search.industry, locality=new_domain_search.locality, year_founded=new_domain_search.year_founded, linkedin=new_domain_search.linkedin)


def fetchPhone(type):
    phone = request.json.get('phoneNumber')
    country = request.json.get('countryCode')
    phone_number_complete = country+phone
    phone_number_list = [item.prefix +
                         item.number for item in Phone.query.all()]
    if phone_number_complete in phone_number_list:
        new_phone_search = Phone.query.filter(
            Phone.number == phone).first()
        new_search = Search(search_type=type,
                            phone_search_id=new_phone_search.id)
        db.session.add(new_search)
        db.session.commit()
        db.session.close()
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
        new_search = Search(search_type=type,
                            phone_search_id=new_phone_search.id)
        db.session.add(new_search)
        db.session.commit()
        db.session.close()
    return jsonify(type=type, date=new_search.showdate, phone_number=new_phone_search.number, prefix=new_phone_search.prefix, local=new_phone_search.local, country=new_phone_search.country, location=new_phone_search.location, phone_type=new_phone_search.phone_type, carrier=new_phone_search.carrier)


def fetchEmail(type):
    email_address = request.json.get('emailAddress')
    email_address_list = [item.email for item in Email.query.all()]
    if email_address in email_address_list:
        new_email_search = Email.query.filter(
            Email.email == email_address).first()
        new_search = Search(search_type=type,
                            email_search_id=new_email_search.id)
        db.session.add(new_search)
        db.session.commit()
        db.session.close()
    else:
        response = requests.get(
            f'https://emailvalidation.abstractapi.com/v1/?api_key={EMAIL_KEY}&email={email_address}').json()
        if response['deliverability'] != 'DELIVERABLE':
            return jsonify(type=False)
        else:
            new_email_search = Email(email=email_address, is_valid=response['is_valid_format']['text'].capitalize(), is_free_email=response['is_free_email']['text'].capitalize(), is_disposable=response['is_disposable_email']['text'].capitalize(
            ), is_role=response['is_disposable_email']['text'].capitalize(), is_catchall=response['is_disposable_email']['text'].capitalize(), is_mx_found=response['is_disposable_email']['text'].capitalize(), is_smtp_valid=response['is_disposable_email']['text'].capitalize())
            db.session.add(new_email_search)
            db.session.commit()
            new_search = Search(search_type=type,
                                email_search_id=new_email_search.id)
            db.session.add(new_search)
            db.session.commit()
            db.session.close()
    return jsonify(type=type, date=new_search.showdate, email=new_email_search.email, valid=new_email_search.is_valid, free_email=new_email_search.is_free_email, disposable=new_email_search.is_disposable, role=new_email_search.is_role, catchall=new_email_search.is_catchall, mx=new_email_search.is_mx_found, smtp=new_email_search.is_smtp_valid)
