from flask import Flask, render_template, request, redirect, url_for
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY']='notesapp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/home')
def home():
    return redirect(url_for('hello_world'))


@app.route('/favicon.ico')
def favicon():
    return '', 204


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html')


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)