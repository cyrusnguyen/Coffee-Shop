from flask import Blueprint, flash, render_template, request, url_for, redirect, Markup
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Product, Cart
from .forms import LoginForm, RegisterForm, Updateform
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
            # flash('Logged in successfully!', 'success')
            # if next is None or not nextp.startswith('/'):
            #     return redirect(url_for('index'))
            # return redirect(nextp)
            #flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash(error, 'danger')
    return render_template('auth.html', form = login_form, heading = 'Login')
# Route for registration
@bp.route('/register', methods=['GET','POST'])
def register():
    registration_form = RegisterForm()
    if (registration_form.validate_on_submit() == True):
        #get username, password and email from the form
        uname = registration_form.user_name.data
        pwd = registration_form.password.data
        email = registration_form.email_id.data
        phone_number = registration_form.phone_number.data
        address = registration_form.address.data
        #check if a user exists
        u1 = User.query.filter_by(name=uname).first()
        if u1:
            flash('User name already exists, please login')
            return redirect(url_for('auth.login'))
        #generate_password_hash
        pwd_hash = generate_password_hash(pwd)
        #create a new user model object
        new_user = User(name=uname, password_hash=pwd_hash, email=email, phone_number=phone_number, address=address)
        db.session.add(new_user)
        db.session.commit()
        
        #commit to the database and redirect to HTML page
        return redirect(url_for('main.index'))
    #the else is called when there is a get message
    else:
        return render_template('auth.html', form=registration_form, heading='Register')

@bp.route('/view-profile', methods=['GET','POST'])
@login_required
def view_profile():
    user_carts = Cart.query.filter_by(user_id=current_user.user_id).all()
    return render_template('user.html', user_carts=user_carts)

@bp.route('/update-user', methods=['GET','POST'])
@login_required
def update_user():
    UpdateUserForm = Updateform()
    if (UpdateUserForm.validate_on_submit() == True):
        
        uname = UpdateUserForm.user_name.data
        pwd = UpdateUserForm.password.data
        email = UpdateUserForm.email_id.data
        phone_number = UpdateUserForm.phone_number.data
        address = UpdateUserForm.address.data
        pwd_hash = generate_password_hash(pwd)
        db.session.query(User).filter_by(user_id=current_user.user_id).update(dict(
            name=uname, password_hash=pwd_hash, email=email, phone_number=phone_number, address=address
        ))
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        return render_template('update_user.html', form=UpdateUserForm, heading="Update Profile")
    

# Route for logging out
@bp.route('/logout')
def logout():
    logout_user()
    #flash('Logged out successfully!', 'success')
    return render_template('logout.html')