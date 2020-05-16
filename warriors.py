from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/successstories')
def successstories():
    return render_template('successstories.html')

@app.route('/virtual_coach')
def virtual_coach():
    return render_template('virtual_coach.html')

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


if __name__ == '__main__':
    app.run(debug=True)
    