from urllib.parse import quote_plus
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "firstapp"
password = "FirstApp@123"
password_encoded = quote_plus(password)
    

def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://root:{password_encoded}@localhost/{DB_NAME}?charset=utf8mb4"
    )
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #JWT CONFIG
    app.config['JWT_SECRET_KEY'] = "super-secret-key"
    db.init_app(app)


    from .views import views
    from .auth import auth
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/auth')

       #  ADD THIS HERE
    @app.route('/login')
    def login_redirect():
        return redirect(url_for('auth.login'))
    
    @app.route('/sign-up')
    def signup_redirect():
        return redirect(url_for('auth.sign_up'))  

    from .models import User,Note
    
     # ----------------------------
    # Flask-Login setup (FIX)
    # ----------------------------
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'   # redirect if not logged in
    login_manager.init_app(app)
    
     # ----------------------------
    # User loader (REQUIRED)
    # ----------------------------
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    create_database(app)

    return app


def create_database(app):
      with app.app_context():
         db.create_all()
         print('Created Database!')  