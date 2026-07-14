from flask import Flask, render_template, request, redirect, url_for
from models import User, Note #importing the models to know about the tables and sqlalchemy
from extensions import db
from config import config
import os


def create_app():


    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    #creates the instance folder if it doesn't exit
    os.makedirs(app.instance_path,exist_ok=True)

    
    from routes.auth import auth_bp
    from routes.notes  import notes_bp
    from routes.api import api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(api_bp)
    





    @app.route('/')
    def hello_world():
        return """
        <h1>Hello World!</h1>
        <p>My notes app</p>
        <p>project start up done and database connected</p> """

    



    with app.app_context():
        db.create_all()
    return app
app=create_app()

if __name__ == '__main__':
    app.run(debug=True)