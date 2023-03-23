#import flask - from the package import class
from flask import Flask, session
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Blueprint, render_template
from datetime import timedelta


app = Flask(__name__)
db = SQLAlchemy(app)
def create_app():
  
    
    app.debug = True
    app.secret_key ='supersecretkey'
    # #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Product.db?check_same_thread=False'
    # #initialize db with flask app
    db.init_app(app)
    with app.app_context():
        from .models import Product, Comment, User, Cart, Category, Anonymous
        db.create_all()
        db.session.commit()

    bootstrap = Bootstrap5(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    # Set session timeout to 5mins
    login_manager.login_view='auth.login'
    login_manager.anonymous_user = Anonymous
    login_manager.needs_refresh_message = (u"Session timedout, please re-login")
    login_manager.needs_refresh_message_category = "info"
    login_manager.init_app(app)
    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=45)
    
    

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)
    from . import products
    app.register_blueprint(products.productbp)
    from . import auth
    app.register_blueprint(auth.bp)

    from . import cart
    app.register_blueprint(cart.cartbp)
   
    
    return app

@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
  return render_template("404.html")

