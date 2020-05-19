from flask import Blueprint, render_template, redirect, url_for
from warriorsproject import db 
from warriorsproject.models import Runners
from warriorsproject.runners.forms import AddForm, DelForm

runners_blueprint = Blueprint('runners', __name__, template_folder='templates/runners')


@runners_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    
    form = AddForm()
    
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        age = form.age.data
        group = form.group.data 
        new_runner = Runners(firstname, lastname, age, group)
        db.session.add(new_runner)
        db.session.commit()
        
        return redirect(url_for('runners.list'))
        
    return render_template('add_runner.html', form=form)   


@runners_blueprint.route('/list')
def list():
    
    runners = Runners.query.all()
    return render_template('list_runners.html', runners=runners)


@runners_blueprint.route('/delete', methods=['GET', 'POST'])
def delete():
    
    form = DelForm()
    
    if form.validate_on_submit():
        
        id = form.id.data
        runner = Runners.query.get(id)
        db.session.delete(runner)
        db.session.commit()
        
        return redirect(url_for('list_runners'))
    return render_template('delete_runner.html', form=form)