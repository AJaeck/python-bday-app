# Flask docs @ https://flask.palletsprojects.com/en/2.0.x/
from email.mime import image
import re
from sre_constants import SUCCESS
from unicodedata import name
from urllib import response
from flask import Flask, request, render_template, redirect, flash, jsonify
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import pymsteams


# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
from dotenv import load_dotenv
load_dotenv()

#Import WTForms https://flask-wtf.readthedocs.io/en/1.0.x/
from forms import GW_Form, Upload_Form

# Sendinblue API Docs: https://developers.sendinblue.com/reference/
import sib_api_v3_sdk 
import requests
base = "https://api.sendinblue.com/v3/"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "api-key": os.getenv("SIB_Key")
}

# Initialie Imagekit.io: https://github.com/imagekit-developer/imagekit-python
from imagekitio import ImageKit
imagekit = ImageKit(
    private_key=os.getenv("IK_Private_Key"),
    public_key=os.getenv("IK_Public_Key"),
    url_endpoint = os.getenv("IK_Endpoint")
)

# You must create the connectorcard object with the Microsoft Webhook URL
myTeamsMessage = pymsteams.connectorcard(os.getenv("TEAMS_URL"))

# initiate flask app and Config Variables
# recaptcha keys and csrf protection
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET")
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv("SITEKEY")
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv("SECRETKEY")
app.config['UPLOAD_FOLDER'] = 'static/images/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 250 * 1024 * 1024 # 25MB
app.config['UPLOAD_EXTENSIONS'] = ['.png', '.jpg', '.jpeg', '.gif', '.svg']

# create routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/send-pics', methods=["GET", "POST"])
def send_pics(): 
    form = Upload_Form()
    image_numbers = 0

    if form.validate_on_submit():
        images = form.file.data
        for i in images:
            image_filename = secure_filename(i.filename)
            if image_filename != '':
                file_ext = os.path.splitext(image_filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    print(f'File Extension {file_ext} not supported')
                    continue
                # Image save to static image folder
                image_name = str(uuid.uuid1()) + "_" + image_filename
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name) 
                i.save(image_path)
                image_numbers += 1

        if image_numbers > 1:
            flash(f'{image_numbers} Bilder wurden erfolgreich hochgeladen', 'success')
            # Title
            myTeamsMessage.title("New Media Upload")
            # Add text to the message.
            myTeamsMessage.text(f'{image_numbers} media items were uploaded to server')
            # send the message to MS Teams.
            myTeamsMessage.send()
        elif image_numbers == 1:

            flash(f'{image_numbers} Bild wurde erfolgreich hochgeladen', 'success')
            # Title
            myTeamsMessage.title("New Media Upload")
            # Add text to the message.
            myTeamsMessage.text(f'{image_numbers} media item was uploaded to the server')
            # send the message to MS Teams.
            myTeamsMessage.send()
        else:
            flash('Es wurde kein Bild ausgewählt.', 'danger')

    return render_template("send-pics.html", form=form, extensions=app.config['UPLOAD_EXTENSIONS'])

@app.route("/send-pics/uploads", methods=["GET", "POST"])
def upload_pics():

    upload_sucessfull = bool(request.args['upload'])

    if request.method == "POST" and upload_sucessfull == True:

        upload_number = 0
        upload_files = os.listdir('./' + app.config['UPLOAD_FOLDER'])
        
        for u in upload_files:

            image_name = u
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)

            upload = imagekit.upload(
                file=open(image_path, "rb"),
                file_name=image_name
            )
            print("Upload binary", upload)

            if upload['error'] != None:
                print('Error: ' + upload['error']['message'])
            else:
                upload_number += 1
                os.remove(image_path)
                print("Remove Temp Image" + " #" + str(upload_number) + ' ' + image_name)

        if upload_number > 1:
            # Title
            myTeamsMessage.title("New Media Upload")
            # Add text to the message.
            myTeamsMessage.text(f'{upload_number} media items were uploaded to Imagekit')
            # send the message to MS Teams.
            myTeamsMessage.send()
        elif upload_number == 1:
            # Title
            myTeamsMessage.title("New Media Upload")
            # Add text to the message.
            myTeamsMessage.text(f'{upload_number} media item was uploaded to Imagekit')
            # send the message to MS Teams.
            myTeamsMessage.send()
        else:
            # Title
            myTeamsMessage.title("Error with Media Upload")
            # Add text to the message.
            myTeamsMessage.text('No media items were uploaded to Imagekit')
            # send the message to MS Teams.
            myTeamsMessage.send()
    return redirect('/')

@app.route('/send-wishes', methods=["GET", "POST"])
def send_wishes():    
    form = GW_Form()
    # form data
    fname=form.fname.data
    lname=form.lname.data
    email=form.email.data
    gw_text=form.gw_text.data
    if form.validate_on_submit():  
        # Send Confirmation Email with SIB
        url_add_contact = base + "contacts/doubleOptinConfirmation"
        payload = {
                "attributes": {
                    "VORNAME": fname,
                    "NACHNAME": lname,
                    "GW_TEXT": gw_text
                },
                "includeListIds": [2],
                "updateEnabled": True,
                "email": email,
                "templateId": 1,
                "redirectionUrl": "https://anna-hat-geburtstag.com/"
        }
        response = requests.request("POST", url_add_contact, json=payload, headers=headers)
        print(f'New form submission from {fname} {lname}')
        print(response.text)

        # MS Teams Card Title
        myTeamsMessage.title(f'New form submission from: {fname} {lname}')
        # Add text to the message.
        myTeamsMessage.text(gw_text)
        # send the message to MS Teams.
        myTeamsMessage.send()

        return redirect('versand', code=307)
    elif form.secret.errors:
        error_statement = "Das war wohl nicht die richtige Antwort auf die Sicherheitsfrage."
        return render_template("send-wishes.html", form=form, error_statement=error_statement, fname=fname, lname=lname, gw_text=gw_text, email=email )
    else:
        print(form.errors)

    return render_template("send-wishes.html", form=form)

@app.route("/versand", methods=["POST", "GET"])
def form():

    if request.method == 'POST':
        form = GW_Form()
        fname=form.fname.data
        email=form.email.data

        return render_template("versand.html", fname=fname, email=email)

    return redirect('/')

@app.route("/gallery")
def gallery():
    
    image_req = imagekit.list_files({
        "skip": 10,
        "limit": 3,
    })

    image_res = image_req['response']
    image_name_list = [name['name'] for name in image_res]
    image_path_list = ""

    for name in image_name_list:
        image_path_list += name + ","

    print (image_path_list)

    return render_template("gallery.html", image_path_list=image_path_list)