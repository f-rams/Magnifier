# Magnifier

- [Magnifier](#magnifier)
  - [Description](#description)
  - [Usage](#usage)
  - [Tech Stack](#tech-stack)
  - [Installation](#installation)
  - [Abstract API](#abstract-api)
 
## Description


### Powerful OSINT Tool for Data Validation and Enrichment

This user-friendly tool empowers security analysts, recruiters, and marketers to validate and enrich data related to phone numbers, emails, VAT registration numbers (limited to the EU), and company domains.

### Validate and Gather Insights:

- Phone Numbers: Check validity, pinpoint location (local & international), identify carrier, and determine phone type (mobile/landline).
- Emails: Verify email validity and distinguish between free and paid accounts.
- VAT Numbers (EU Only): Confirm registration, uncover company name, location, and address.
- Domains: Extract company information, estimate employee count, discover foundation year, and locate LinkedIn profile.

### Technical Backbone:

- Python and Flask: Power the backend, seamlessly interacting with third-party APIs to retrieve data based on user input.
- PostgreSQL Database: Securely stores information gathered from each search for future reference (if applicable).

### Transparency and User Trust:

- Third-Party Data Sources: Leverages reputable third-party API ([Abstract API](https://www.abstractapi.com)) to provide enriched data.
- Data Limitations: Acknowledges potential limitations in data accuracy and completeness based on the user's inpurt.


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

Run the following commands from the capstone directory in this order:

- Requirements:

```shell
$ pip install -r requirements.txt
```

After installing the requirements, run a Python interactive shell to execute a series of commands on the app.py file. Using [Ipython](#https://ipython.org/), run the following commands from the main folder:

- Run the seed.py file to create de database:

```shell
$ %run seed.py
```

## Abstract API

This tool uses a third-party API [(Abstract )](https://www.abstractapi.com) to assess and gather information related to the queries performed by the user.

It uses four different API KEYs for each type of request: phone, email, VAT, and domain. After registering on the website, save the keys on the **app.py** file or save them on a separate file and import them to the first. Assign each key to its respective variable (**PHONE_KEY, EMAIL_KEY, VAT_KEY, DOMAIN_KEY**) or replace it with the key.


