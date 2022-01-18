# Flask docs @ https://flask.palletsprojects.com/en/2.0.x/
from ast import NotIn
from re import X
from unicodedata import name
from flask import Flask, request, render_template, redirect, url_for

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
from dotenv import load_dotenv
import os

#Import WTForms https://flask-wtf.readthedocs.io/en/1.0.x/
from forms import GW_Form

# Sendinblue API Docs: https://developers.sendinblue.com/reference/
import sib_api_v3_sdk 
import requests
base = "https://api.sendinblue.com/v3/"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "api-key": os.getenv("SIB_Key")
}

# take environment variables from .env.
load_dotenv()

# initiate flask app and Config Variables
# recaptcha keys and csrf protection
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET")
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv("SITEKEY")
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv("SECRETKEY")

# create routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/glueckwunsch', methods=["GET", "POST"])
def glueckwunsch():    
    form = GW_Form()

    # form data
    name=form.name.data
    email=form.email.data
    gw_text=form.gw_text.data
    secret=form.secret.data

    if form.validate_on_submit():  
        
        # Send Confirmation Email with SIB
        url_add_contact = base + "contacts/doubleOptinConfirmation"
        payload = {
                "attributes": {
                    "VORNAME": name,
                    "GW_TEXT": gw_text
                },
                "includeListIds": [2],
                "updateEnabled": True,
                "email": email,
                "templateId": 1,
                "redirectionUrl": "http://127.0.0.1:5000/"
        }
        response = requests.request("POST", url_add_contact, json=payload, headers=headers)
        print("New Form Submission from: " + name)
        print(response.text)
        return redirect('versand', code=307)
    elif form.secret.errors:
        error_statement = "Das war wohl nicht die richtige Antwort auf die Sicherheitsfrage."
        return render_template("glueckwunsch.html", form=form, error_statement=error_statement, name=name, gw_text=gw_text, email=email )
    else:
        print(form.errors)

    return render_template("glueckwunsch.html", form=form)

@app.route("/versand", methods=["POST", "GET"])
def form():

    if request.method == 'POST':
        form = GW_Form()
        name=form.name.data
        email=form.email.data

        return render_template("versand.html", name=name, email=email)

    return redirect('/')


@app.route("/real", methods=["POST"])
def success():
    form = GW_Form()

    name=form.name.data
    email=form.email.data
    gw_text=form.gw_text.data
    secret=form.secret.data

    if form.validate_on_submit():                

        url_add_contact = base + "contacts/doubleOptinConfirmation"
        payload = {
                "attributes": {
                    "VORNAME": name,
                    "GW_TEXT": gw_text
                },
                "includeListIds": [2],
                "updateEnabled": True,
                "email": email,
                "templateId": 1,
                "redirectionUrl": "http://127.0.0.1:5000/"
        }
        response = requests.request("POST", url_add_contact, json=payload, headers=headers)
        print("New Form Submission from: " + name)
        print(response.text)

    return render_template("versand.html", name=name, email=email)
