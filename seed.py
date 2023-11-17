from models import db
from app import app
from models import Country, Vat_Country
from countries import country_vat_codes, country_phone_codes
app.app_context().push()


db.drop_all()
db.create_all()


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


get_phone_pair(country_phone_codes)

get_vat_pair(country_vat_codes)
