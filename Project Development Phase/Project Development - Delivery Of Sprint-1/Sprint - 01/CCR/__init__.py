from flask import Flask, session
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "PHqtYfAN2v"

    # registering the blue prints with the app
    from .views import views
    app.register_blueprint(views, appendix='/')

    from .cust import cust
    app.register_blueprint(cust, appendix='/customer/')

    from .admin import admin
    app.register_blueprint(admin, appendix='/admin/')

    # setting up the login manager
    login_manager = LoginManager()
    login_manager.login_view = "blue_print.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        if session.get('LOGGED_IN_AS') is not None:
            if session['LOGGED_IN_AS'] == "CUSTOMER":
                from .views import customer
                return customer

        else:
            return None

    return 
