# Flask docs @ https://flask.palletsprojects.com/en/2.0.x/
from unicodedata import name
from flask import Flask, request, render_template, redirect, flash
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import base64

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

# set file upload definitions
UPLOAD_FOLDER = 'static/images/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# initiate flask app and Config Variables
# recaptcha keys and csrf protection
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET")
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv("SITEKEY")
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv("SECRETKEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024 # 25MB

# create routes
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/auth', methods=["GET", "POST"])
def auth():
    imagekit = ImageKit(
    private_key=os.getenv("IK_Private_Key"),
    public_key=os.getenv("IK_Public_Key"),
    url_endpoint = os.getenv("IK_Endpoint")
    )

    auth_params = imagekit.get_authentication_parameters()

    print("Auth params-", auth_params)

@app.route('/send-pics', methods=["GET", "POST"])
def send_pics(): 

    form = Upload_Form()
    image_numbers = 0
    print(app.config['UPLOAD_FOLDER'])
    image_name="bild.jpg"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name) 
    print(image_path)

    if form.validate_on_submit():
        images = form.file.data
        for i in images:
            # Image save to static image folder
            image_filename = secure_filename(i.filename)
            image_name = str(uuid.uuid1()) + "_" + image_filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name) 
            i.save(image_path)
            # Upload Image to Imagekit
            upload = imagekit.upload(
                file=open(image_path, "rb"),
                file_name=image_name,
                options={
                "response_fields": ["is_private_file", "tags"],
                "tags": ["tag1", "tag2"]
                },
            )
            print("Upload binary", upload)
            os.remove(image_path)
            print("Remove Temp Image" + " #" + str(image_numbers) + ' ' + image_name)
            if upload['error'] != None:
                print('Error: ' + upload['error']['message'])
            else:
                image_numbers += 1
        if image_numbers > 1:
            flash(f'{image_numbers} Bilder wurden erfolgreich hochgeladen', 'success')
        elif image_numbers == 1:
            flash(f'{image_numbers} Bild wurde erfolgreich hochgeladen', 'success')
        else:
            flash('Es wurde kein Bild ausgewählt.', 'danger')
    return render_template("send-pics.html", form=form, extensions=ALLOWED_EXTENSIONS)

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
        print("New Form Submission from:" + fname + lname)
        print(response.text)
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
