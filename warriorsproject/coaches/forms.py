from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField, SelectField, TextField, 
                     TextAreaField, SubmitField, IntegerField)
from wtforms.validators import DataRequired, InputRequired

class AddForm(FlaskForm):
    
    firstname = StringField('First Name: ')
    lastname = StringField('Last Name: ')
    submit = SubmitField('Add Coach') 