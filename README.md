# Magnifier

- [Magnifier](#magnifier)
  - [Description](#description)
  - [Usage](#usage)
  - [Tech Stack](#tech-stack)
  - [Installation](#installation)
  - [Abstract API](#abstract-api)
 
## Description

This tool validates queries on phone numbers, emails, VAT registration numbers (only for the EU), and companies' internet domains. It's supposed to work as a lightweight OSINT (open-source investigation) tool that evaluates the data provided by the user and returns public information regarding it.

The following information can be retrieved based on each asset:

- Phone number: phone validity, phone local and international location, carrier, type

- Email: email validity, free/paid plan.

- VAT: company name, location, address (only for EU)

- Domain: company name, location, number of employees, foundation year, LinkedIn

The app works mainly with Python and Flask on the back end to send requests to the third-party API and retrieve data pertaining to the user input. PostgreSQL is to store data related to each search.

## Usage

Select the type of query that you want to perform and type the asset to be validated.

- Phone Query: Select the country and type the phone number, including the local code

- Email query: Type the email address

- VAT number: Select the country code and type the company's VAT number

- Domain: Type the domain of the subject to be researched

Each result is automatically saved in the user's section, accessed anytime from the navbar. Since all results come from a third-party validation API, they can't be edited or manipulated.

## Tech Stack

This application was developed with the support of the following tools:

- Programming languages: JavaScript, [Python](https://www.python.org)
- Database storage and management: [PostgreSQL](https://www.postgresql.org), [Postico](https://eggerapps.at/postico2/)
- Frontend libraries: [Booststrap](https://getbootstrap.com), [jQuery](https://jquery.com),
- HTTP Client: [Axios](https://axios-http.com/docs/intro)
- Backend libraries: [Jinja](https://jinja.palletsprojects.com/en/3.1.x/)
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


