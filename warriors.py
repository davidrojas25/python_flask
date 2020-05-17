import os
from flask import Flask, render_template, request, session, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField, SelectField, TextField, 
                     TextAreaField, SubmitField, IntegerField)
from wtforms.validators import DataRequired, InputRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app,db) # so you can make changes to actual db
# steps to migrate are - flask db migrate -m "something" then flask db upgrade

class Runners(db.Model):
    # manual table name choice
    __tablename__ = 'runners'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    age = db.Column(db.Integer)
    group = db.Column(db.Text)
    runs = db.relationship('Run', backref='runner', lazy='dynamic') # one to many
    coach = db.relationship('Coach', backref='runner', uselist=False) #one to one
    
    
    def __init__(self, firstname, lastname, age, group):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.group = group
        
    def __repr__(self):
        if self.coach:
            return f"Runner's name is {self.firstname} {self.lastname} and coach is {self.coach.firstname}"
        else:
            return f"Runner's name is {self.firstname} {self.lastname} and has no coach yet!" 
        
    def report_runs(self):
       print("Here are my runs:")
       for run in self.runs:
           print(run.item_name)     
            
    
class Run(db.Model):
    
    __tablename__ = 'runs'
    
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)
    runner_id = db.Column(db.Integer, db.ForeignKey('runners.id'))
    
    def __init__(self, item_name, runner_id):
        self.item_name = item_name
        self.runner_id = runner_id
        
    

class Coach(db.Model):
    __tablename__ = 'coaches'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text)
    runner_id = db.Column(db.Integer, db.ForeignKey('runners.id'))   
    
    def __init__(self, firstname, runner_id):
        self.firstname = firstname
        self.runner_id = runner_id

class pacing1600(FlaskForm):
    
    first = StringField('What is your first name?', validators=[DataRequired()])
    last = StringField('What is your last name?', validators=[DataRequired()])
    target_min = IntegerField('Minutes:', validators=[DataRequired()])
    target_sec = IntegerField('Seconds:', validators=[InputRequired()])
    strategy = SelectField(u'Select your racing strategy:',
                           choices=[('front_runner', 'Front Runner'), ('even_pace', 'Even Pace'), ('off_pace', 'Run from Behind')])
    submit = SubmitField('Submit')
     

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/successstories')
def successstories():
    return render_template('successstories.html')

@app.route('/virtual_coach', methods=['GET', 'POST'])
def virtual_coach():
    
    form = pacing1600()
    
    if form.validate_on_submit():
        session['first'] = form.first.data
        session['last'] = form.last.data
        session['target_min'] = form.target_min.data
        session['target_sec'] = str(form.target_sec.data).zfill(2)
        session['strategy'] = form.strategy.data
        session['total_sec'] = form.target_min.data * 60 + form.target_sec.data
        avg_sec = int((form.target_min.data * 60 + form.target_sec.data)/4)
        if form.strategy.data == 'even_pace':
          session['perlapmin'] = int(avg_sec//60)
          session['perlapsec'] = str(int(avg_sec%60)).zfill(2)
        elif form.strategy.data == 'front_runner':
          session['fr_lap1min'] = int((avg_sec*.88)//60)
          session['fr_lap1sec'] = str(int((avg_sec*.88)%60)).zfill(2) 
          session['fr_lap2min'] = int((avg_sec*.94)//60)
          session['fr_lap2sec'] = str(int((avg_sec*.94)%60)).zfill(2)
          session['fr_lap3min'] = int((avg_sec*1.09)//60)
          session['fr_lap3sec'] = str(int((avg_sec*1.09)%60)).zfill(2)
          session['fr_lap4min'] = int((avg_sec*1.09)//60)
          session['fr_lap4sec'] = str(int((avg_sec*1.09)%60)).zfill(2)
        elif form.strategy.data == 'off_pace':
          session['op_lap1min'] = int(avg_sec//60)
          session['op_lap1sec'] = str(int(avg_sec%60)).zfill(2)
          session['op_lap2min'] = int((avg_sec*1.06)//60)
          session['op_lap2sec'] = str(int((avg_sec*1.06)%60)).zfill(2)
          session['op_lap3min'] = int((avg_sec*1.05)//60)
          session['op_lap3sec'] = str(int((avg_sec*1.05)%60)).zfill(2)
          session['op_lap4min'] = int((avg_sec*.89)//60)
          session['op_lap4sec'] = str(int((avg_sec*.89)%60)).zfill(2) 
        
        
        return redirect(url_for('paceplan1600')) 
    
    return render_template('virtual_coach.html', form=form)

@app.route('/paceplan1600')
def paceplan1600():
    return render_template('paceplan1600.html')

@app.route('/teampics')
def teampics():
    return render_template('teampics.html')

@app.route('/warriors')
def warriors():
    return render_template('warriors.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/trainingpacecal')
def trainingpacecal():
    return render_template('trainingpacecal.html')

@app.route('/pacechart')
def pacechart():
    return render_template('pacechart.html')

@app.route('/thankyou')
def thankyou():
    first = request.args.get('first')
    last = request.args.get('last')
    return render_template('thankyou.html', first=first, last=last)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
    