from asyncio import events
from multiprocessing.dummy import current_process
from re import X
from flask import Blueprint, render_template, url_for, redirect, request
from sqlalchemy.orm import load_only
from flask_login import login_required, current_user
from website.forms import ContactUsForm, BasicInfoForm, Updateform
from .models import Product, User, Cart, Category, ContactUs
from sqlalchemy import desc
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    featured_products = db.session.query(Product, Category.name.label("category_name")).join(Category, Product.category_id == Category.category_id, isouter=True).limit(3).all()
    print(featured_products)
    latest_products = db.session.query(Product, Category.name.label("category_name")).join(Category, Product.category_id == Category.category_id, isouter=True).order_by(desc(Product.released_date)).limit(6).all()
    latest_product = db.session.query(Product, Category.name.label("category_name")).join(Category, Product.category_id == Category.category_id, isouter=True).order_by(desc(Product.sold_quantity)).limit(1).all()
    
    return render_template('home.html', featured_products=featured_products, latest_products = latest_products, latest_product = latest_product)

@bp.route('/success')
def success():
    return render_template('success.html')



@bp.route('/user-history', methods=['GET', 'POST'])
def user_history():
    print('Method type: ', request.method)
    cu_form = ContactUsForm()
    UserTickets = Cart.query.filter_by(user = current_user).all()
    product = Product.query.filter(Product.user_id == current_user.id and Product.status ==  "Unpublished")
    productID = []
    TicketsProduct = []     
    productID.append(1)#Throwaway data 
    for x in range(len(UserTickets)):
        productID.append(UserTickets[x].id)
        TicketsProduct = TicketsProduct + Product.query.filter((Product.id ==UserTickets[x].product_id)).all()
    
    if cu_form.validate_on_submit():

        print('Successfully sent message', 'success')
        return redirect(url_for('main.user_history'))

    return render_template('user_history.html', form=cu_form, user_products = TicketsProduct  , shown_amount = productID, product = product)

@bp.route('/update-user', methods=['GET', 'POST'])
@login_required
def update_user():
    registration_form = Updateform()
    
    if (registration_form.validate_on_submit() == True):
        uname = registration_form.user_name.data
        pwd = registration_form.password.data
        email = registration_form.email_id.data
        phone_number = registration_form.phone_number.data

        address = registration_form.address.data


        

        
        # Generate password hash - Not the raw password
        pwd_hash = generate_password_hash(pwd)
        

        update = User.query.filter_by(id = current_user.id).update(dict(name=uname, password_hash=pwd_hash, emailid=email, phone_number = phone_number, address = address))


        db.session.commit()
        
        # Commit to the database and redirect to HTML page
        return redirect(url_for('main.user_history'))
    # Else is called when there is a get message
    else:
        return render_template('user.html', form=registration_form, heading='Update Profile')
# General search
@bp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        dest = "%" + request.args['search'] + '%'
        search_results = Product.query.filter((Product.description.like(dest))|(Product.name.like(dest))).order_by(desc(Product.name)).all()
        return render_template('search_results.html', search_results=search_results)
    else:
        return redirect(url_for('main.index'))

# Search by style
@bp.route('/filterStyle')
def filterStyle():
    if request.args['filterStyle']:
        print(request.args['filterStyle'])
        dest = "%" + request.args['filterStyle'] + '%'
        search_results = Product.query.filter(Product.style.like(dest))
        return render_template('search_results.html', search_results=search_results)
    else:
        return redirect(url_for('main.index'))

# Search by status
@bp.route('/filterStatus')
def filterStatus():
    if request.args['filterStatus']:
        print(request.args['filterStatus'])
        dest = "%" + request.args['filterStatus'] + '%'
        search_results = Product.query.filter(Product.status.like(dest))
        return render_template('search_results.html', search_results=search_results)
    else:
        return redirect(url_for('main.index'))

# for product view look at Products.py@mainbp.route('/search')
@bp.route('/products/page=<int:page_num>')
@bp.route('/products/')
def show_all(page_num=1):
    all_products_query = db.session.query(Product, Category.name.label("category_name")).join(Category, Product.category_id == Category.category_id, isouter=True).filter(Product.status ==  "Available")
    total_products = len(all_products_query.all())
    all_products = all_products_query.paginate(per_page=12, page=page_num)
    return render_template('search_results.html', search_results=all_products, total_products=total_products)

@bp.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    contact_us_form = ContactUsForm()
    if (contact_us_form.validate_on_submit()):
        #get username, password and email from the form
        uname = contact_us_form.user_name.data
        email = contact_us_form.email.data
        subject = contact_us_form.subject.data
        message = contact_us_form.message.data
        contact_us = ContactUs(user_name=uname, email=email, subject=subject, message=message)
        db.session.add(contact_us)

        db.session.commit()
        
        #commit to the database and redirect to HTML page
        return redirect(url_for('main.success'))

    else:
        return render_template('contact_us.html', form=contact_us_form)
