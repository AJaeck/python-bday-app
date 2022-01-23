from flask_wtf import RecaptchaField, FlaskForm
from wtforms import StringField, TextAreaField, EmailField, MultipleFileField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed

# Form ORM
class GW_Form(FlaskForm):
    
    name = StringField('Name', validators=[
        DataRequired(message=('Du hast deinen Namen vergessen dum dum 🤓')),
        ])

    email = EmailField('E-Mail', validators=[
        DataRequired('Ohne E-Mail ohne mich 😡'),
        Email('Was soll das für 1 E-Mail sein 😶?')
        ])

    gw_text = TextAreaField('Versende deine Glückwünsche? (max. 2000 Zeichen)', validators=[
        DataRequired(message=('Upps...Du hast die Glückwünsche vergessen 🙊')),
        Length(min=5, message=('Text zu kurz')),
        Length(max=2000, message=('Text zu lang'))
    ])

    secret = StringField('Wie heißt Annas Hund? (Sicherheitsfrage)', validators=[
    DataRequired('Beantworte bitte die Sicherheitsfrage du Bot 🤖')
    ])

    recaptcha=RecaptchaField()

    def validate_secret(self, secret):
        secret_list = ['Hailey', 'hailey']
        if secret.data not in secret_list:
            raise ValidationError('Das war die falsche Antwort 😪')

class Upload_Form(FlaskForm):
    file = MultipleFileField('Lade ein Bild hoch', validators=[
        FileAllowed(['png', 'jpg', 'jpeg', 'gif', 'svg'], 'Es sind nur folgende Formate erlaubt: .png, .jpg, .jpeg, .gif, .svg')
    ])
