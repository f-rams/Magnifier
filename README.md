# Magnifier

- [Magnifier](#magnifier)
  - [Description](#description)
  - [Usage](#usage)
  - [Tech Stack](#tech-stack)
  - [Installation](#installation)
  - [Abstract API](#abstract-api)
  - [Endpoints](#endpoints)
 
## Description


### OSINT Tool for Data Validation and Enrichment

This user-friendly tool empowers security analysts, recruiters, and marketers to validate and enrich data related to phone numbers, emails, VAT registration numbers (limited to the EU), and company domains.

### Features

Validate and Gather Insights:

- Phone Numbers: Check validity, pinpoint location (local & international), identify carrier, and determine phone type (mobile/landline).
- Emails: Verify email validity and distinguish between free and paid accounts.
- VAT Numbers (EU Only): Confirm registration, uncover company name, location, and address.
- Domains: Extract company information, estimate employee count, discover foundation year, and locate LinkedIn profile.

Backend and Data Management:

- Python and Flask: Backend language and web framework to connect with Abstract API to retrieve data based on user input.
- PostgreSQL Database: Securely stores information gathered from each search for future reference (if applicable).

Transparency and User Trust:

- Third-Party Data Sources: Leverages third-party API ([Abstract API](https://www.abstractapi.com)) to provide enriched data.

## Usage

This user guide outlines the intuitive process of using our data validation tool:

Choose Your Validation Type:

- Phone: Select the country and enter the phone number, including the local area code.
- Email: Simply type the email address you want to verify.
- VAT Number (EU Only): Choose the relevant country code and enter the company's VAT number.
- Domain: Type the domain name of the website or organization you wish to research.


## Tech Stack

This application was developed with the support of the following tools:

- Programming languages: JavaScript, [Python](https://www.python.org)
- Database storage and management: [PostgreSQL](https://www.postgresql.org)
- Frontend libraries: [Booststrap](https://getbootstrap.com), [jQuery](https://jquery.com),
- HTTP Client: [Axios](https://axios-http.com/docs/intro)
- Backend libraries: [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- Third-party API: [Abstract API](https://www.abstractapi.com)

## Installation

Create a free account at [Abstract API](https://www.abstractapi.com) and save the API keys for the four different types of queries: phone, domain, email, and VAT.

From the root directory, run the following command:

- Package installment:

```shell
$ pip install -r requirements.txt
```

This application uses a SQL-Alchemy ORM and PostgreSQL database. There is no script that creates the database, so the user needs to provide a database URI to be stored in a .env file in the root directory and later accessed by the SQL-Alchemy in the app.py file. Alternatively, the user can provide the URI directly as a value for "app.config['SQLALCHEMY_DATABASE_URI'] = {URI}" in the app.py file.

- After setting up the database and connecting to it, run the seed.py file:

```shell
$ python3 seed.py
```

## Abstract API

This tool uses a third-party API [(Abstract )](https://www.abstractapi.com) to assess and gather information related to the queries performed by the user.

It uses four different API KEYs for each type of request: phone, email, VAT, and domain. After registering on the website, save the keys on the **app.py** file or save them on a separate env file and import them to the first. Assign each key to its respective variable (**PHONE_KEY, EMAIL_KEY, VAT_KEY, DOMAIN_KEY**).

## Endpoints

Abstract API endpoints (GET only) used for this application:

### Email:

https<area>://emailvalidation.abstractapi.com/v1/?api_key=**EMAIL_KEY**&email=**xyz<area>@email.com**

```
{
    "email": "xyz@email.com",
    "autocorrect": "",
    "deliverability": "DELIVERABLE",
    "quality_score": "0.95",
    "is_valid_format": {
        "value": true,
        "text": "TRUE"
    },
    "is_free_email": {
        "value": true,
        "text": "TRUE"
    },
    "is_disposable_email": {
        "value": false,
        "text": "FALSE"
    },
    "is_role_email": {
        "value": false,
        "text": "FALSE"
    },
    "is_catchall_email": {
        "value": false,
        "text": "FALSE"
    },
    "is_mx_found": {
        "value": true,
        "text": "TRUE"
    },
    "is_smtp_valid": {
        "value": true,
        "text": "TRUE"
    }
}
```

### Phone:  

https<area>://phonevalidation.abstractapi.com/v1/?api_key=**PHONE_KEY**&phone=**17777777777**

```
{
    "phone": "17777777777",
    "valid": true,
    "format": {
        "international": "+17777777777",
        "local": "(777) 777-7777"
    },
    "country": {
        "code": "US",
        "name": "United States",
        "prefix": "+1"
    },
    "location": "San Francisco, California",
    "type": "landline",
    "carrier": "O1 Communications"
}
```

### VAT (EU only):

https<area>://vat.abstractapi.com/v1/validate/?api_key=**VAT_KEY**&vat_number=**SE556656688001**

```
{
    "vat_number": "SE556656688001",
    "valid": true,
    "company": {
        "name": "GOOGLE SWEDEN AB",
        "address": "GOOGLE IRLAND LTD \nM COLLINS, GORDON HOUSE \nBARROW STREET, DUBLIN 4 \nIRLAND"
    },
    "country": {
        "code": "SE",
        "name": "Sweden"
    }
}
```
### Domain:

https<area>://companyenrichment.abstractapi.com/v1/?api_key=**DOMAIN_KEY**&domain=**google.com**

```
{
    "name": "Google",
    "domain": "google.com",
    "year_founded": 1998,
    "industry": "Internet",
    "employees_count": 219238,
    "locality": "Mountain View",
    "country": "United States",
    "linkedin_url": "linkedin.com/company/google"
}
```


