# Flask docs @ https://flask.palletsprojects.com/en/2.0.x/
from ast import NotIn
from flask import Flask, request, render_template

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
from dotenv import load_dotenv
import os


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

# initiate flask app
app = Flask(__name__)

# create routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/glueckwunsch')
def glueckwunsch():
    return render_template("glueckwunsch.html")

@app.route("/versand", methods=["POST"])
def form():

    #form variables
    name = request.form.get("name")
    email = request.form.get("email")
    gw_text = request.form.get("gw_text")
    secret = request.form.get("secret")

    #form error hadling
    if not name or not gw_text or not email or not secret:
        error_statement = "All Form Fields Required...😢"
        return render_template("glueckwunsch.html", error_statement=error_statement, name=name, gw_text=gw_text, email=email )

     #set a list of secrets
    annas_secrets = ["Butter", "butter"]
    if not secret in annas_secrets:
        error_statement = "Das war wohl nicht die richtige Antwort auf die Sicherheitsfrage. Wenn du Hilfe brauchst kontaktiere hubby@anna-mausebaer.de"
        return render_template("glueckwunsch.html", error_statement=error_statement, name=name, gw_text=gw_text, email=email )
        
    #Create Contact via DOI Flow
    url_add_contact = base + "contacts/doubleOptinConfirmation"
    payload = {
            "attributes": {
                "VORNAME": name,
                "GW_TEXT": "gw_text"
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
    
    return render_template("versand.html", name=name)
