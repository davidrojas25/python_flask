from warriorsproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# need to set up db inside of the __init__.py under warriorsproject folder

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# for logins
class User(db.Model, UserMixin):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    
        

class Runners(db.Model):
    # manual table name choice
    __tablename__ = 'runners'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    age = db.Column(db.Integer)
    group = db.Column(db.Text)
    runs = db.relationship('Run', backref='runner', lazy='dynamic') # one to many
    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'))
    
    
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
    miles = db.Column(db.Float)
    timehours = db.Column(db.Integer)
    timemin = db.Column(db.Integer)
    timesec = db.Column(db.Integer)
    runner_id = db.Column(db.Integer, db.ForeignKey('runners.id'))
    
    def __init__(self, item_name, runner_id):
        self.item_name = item_name
        self.runner_id = runner_id
        
    

class Coach(db.Model):
    __tablename__ = 'coaches'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    runners = db.relationship('Runners', backref='coaches', lazy='dynamic') # one to many
      
    
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname