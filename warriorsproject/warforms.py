from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, DateTimeField,
                     RadioField, SelectField, TextField, 
                     TextAreaField, SubmitField, IntegerField)
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo
from wtforms import ValidationError
from warriorsproject.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords must match!')])  
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()]) 
    submit = SubmitField('Register')
    
    def check_email(self, field):
        if User.Query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been already registered!')
        
    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is taken!') 
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
        

class pacing1600(FlaskForm):
    
    first = StringField('What is your first name?', validators=[DataRequired()])
    last = StringField('What is your last name?', validators=[DataRequired()])
    target_min = IntegerField('Minutes:', validators=[DataRequired()])
    target_sec = IntegerField('Seconds:', validators=[InputRequired()])
    strategy = SelectField(u'Select your racing strategy:',
                           choices=[('front_runner', 'Front Runner'), ('even_pace', 'Even Pace'), ('off_pace', 'Run from Behind')])
    submit = SubmitField('Submit')  
    
   
        
           