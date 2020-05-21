from flask import Blueprint, render_template, redirect, url_for
from warriorsproject import db 
from warriorsproject.models import Coach
from warriorsproject.coaches.forms import AddForm

coaches_blueprint = Blueprint('coaches', __name__, template_folder='templates/coaches')


@coaches_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    
    form = AddForm()
    
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        new_coach = Coach(firstname, lastname)
        db.session.add(new_coach)
        db.session.commit()
        
        return redirect(url_for('coaches.list'))
        
    return render_template('add_coach.html', form=form) 


@coaches_blueprint.route('/list')
def list():
    
    coaches = Coach.query.all()
    return render_template('list_coaches.html', coaches=coaches)
