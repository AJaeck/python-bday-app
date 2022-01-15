# Flask docs @ https://flask.palletsprojects.com/en/2.0.x/
from flask import Flask, request, render_template

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
from dotenv import load_dotenv
import os

# Sendinblue API Docs: https://developers.sendinblue.com/reference/
import sib_api_v3_sdk 
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/glueckwunsch')
def glueckwunsch():
    return render_template("glueckwunsch.html")

@app.route("/versand", methods=["POST"])
def form():

    name = request.form.get("name")
    email = request.form.get("email")
    gw_text = request.form.get("gw_text")
    secret = request.form.get("secret")

    #form error hadling
    if not name or not gw_text or not email or not secret:
        error_statement = "All Form Fields Required...😢"
        return render_template("glueckwunsch.html", error_statement=error_statement, name=name, gw_text=gw_text, email=email )
    

    
    return render_template("versand.html", name=name)
