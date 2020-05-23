from warriorsproject import app, db, mail
from flask import render_template, session, request, redirect, url_for, flash, abort
from warriorsproject.warforms import pacing1600, LoginForm, RegistrationForm, ContactUsForm
from warriorsproject.models import User
from flask_login import login_user, login_required, logout_user
from flask_mail import Message
from werkzeug.utils import secure_filename
import os

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/welcome')
#@login_required
def welcome_user():
    return render_template('welcome_user.html')
    
@app.route('/logout')
#@login_required
def logout():
    logout_user()
    flash('You are logged out!')
    return redirect(url_for('index'))  

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)
   
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for Registeration!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)    
    

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

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    
    form = ContactUsForm()
    
    if form.validate_on_submit():
        session['first'] = form.first.data
        session['last'] = form.last.data
        session['email'] = form.email.data
        session['phonenum'] = form.phonenum.data
        session['message'] = form.message.data
        msg = Message('New Warrior Contact Us Message', recipients=['wareliteracing@gmail.com'], reply_to=session['email'])
        msg.body = session['message']
        if form.file.data != None:
            file = form.file.data
            filename = secure_filename(form.file.data.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with app.open_resource(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as fp:
              msg.attach(filename, "image/png", fp.read())
        mail.send(msg)
        
        flash('Thanks for the Message! We will get back to you soon!')
        return redirect(url_for('thankyou'))
        
    return render_template('contactus.html', form=form)

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
