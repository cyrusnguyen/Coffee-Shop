from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, current_user, logout_user
from . import db

bp = Blueprint('auth', __name__)


# Route for logging in
@bp.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    error = None
    if (login_form.validate_on_submit() == True):
        # Get the username and password from the database.
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        if u1 is None:
            error = 'Incorrect user name'

        elif not check_password_hash(u1.password_hash, password):
            error = 'Incorrect password'
        if error is None:

            login_user(u1)
            
            # nextp = request.args.get('next') #this gives the url from where the login page was accessed
            # print(nextp)
            # flash('Logged in successfully!', 'success')
            # if next is None or not nextp.startswith('/'):
            #     return redirect(url_for('index'))
            # return redirect(nextp)
            #flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash(error, 'danger')
    return render_template('user.html', form = login_form, heading = 'Login')
# Route for registration
@bp.route('/register', methods=['GET','POST'])
def register():
    registration_form = RegisterForm()
    if (registration_form.validate_on_submit() == True):
        #get username, password and email from the form
        uname = registration_form.user_name.data
        pwd = registration_form.password.data
        email = registration_form.email_id.data
        #check if a user exists
        u1 = User.query.filter_by(name=uname).first()
        if u1:
            flash('User name already exists, please login')
            return redirect(url_for('auth.login'))
        # don't store the password - crgenerate_password_hasheate password hash
        pwd_hash = generate_password_hash(pwd)
        #create a new user model object
        new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
        db.session.add(new_user)
        db.session.commit()
        
        #commit to the database and redirect to HTML page
        return redirect(url_for('main.index'))
    #the else is called when there is a get message
    else:
        return render_template('user.html', form=registration_form, heading='Register')

# Route for logging out
@bp.route('/logout')
def logout():
    logout_user()
    #flash('Logged out successfully!', 'success')
    return render_template('logout.html')