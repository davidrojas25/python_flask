from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> Hello Puppy!</h1>'

@app.route('/information')
def info():
    return '<h1> Puppies are Cute!</h1>'

@app.route('/puppy/<name>')
def puppy(name):
    if name[-1] == 'y':
        puppylatin = name[:-1] + 'iful'
    else:
        puppylatin = name + 'y'
        
    return "<h1>your puppy latin name is {}!</h1>".format(puppylatin)

if __name__ == '__main__':
    app.run()