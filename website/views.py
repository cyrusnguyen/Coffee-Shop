from asyncio import events
from multiprocessing.dummy import current_process
from re import X
from flask import Blueprint, Markup, render_template, url_for, redirect, request, session
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
    latest_products = db.session.query(Product, Category.name.label("category_name")).join(Category, Product.category_id == Category.category_id, isouter=True).order_by(desc(Product.released_date)).limit(6).all()
    latest_product = db.session.query(Product, Category.name.label("category_name")).join(Category, Product.category_id == Category.category_id, isouter=True).order_by(desc(Product.sold_quantity)).limit(1).all()
    
    return render_template('home.html', featured_products=featured_products, latest_products = latest_products, latest_product = latest_product)

@bp.route('/success')
def success():
    home_url = url_for('main.index')
    error_message = '''<div class="container">
    <h1>Request Successfully Sent!</h1>
    <p>We have received your request. Thank you</p>
    <p>Click <a href="{0}">Here</a> to go back to Home Page </p>
    </div>'''.format(home_url)
    return render_template('blank.html', Message = Markup(error_message))




@bp.route('/products/page=<int:page_num>', methods=['GET','POST'])
@bp.route('/products/', defaults={'page_num': 1}, methods=['GET','POST'])
def show_products(page_num=1):
    
    search_results_query = db.session.query(Product, Category.name.label("category_name")).join(Category, Product.category_id == Category.category_id, isouter=True).filter(Product.status ==  "Available")
    all_products = search_results_query.paginate(per_page=12, page=page_num)
    total_products = len(search_results_query.all())
    return render_template('all_products.html', search_results = all_products, total_products = total_products)
    

@bp.route('/search/page=<int:page_num>', methods=['GET', 'POST'])
@bp.route('/search/', methods=['GET', 'POST'])
def search_products(page_num=1):
    if request.form.get('product_search'):
        search_query = "%" + str(request.form.get('product_search')) + "%"
        session['search'] = str(request.form.get('product_search'))
    else:
        search_query = "%" + session['search'] + '%'
    
    
    search_results_query = db.session.query(Product, Category.name.label("category_name")).\
            join(Category, Product.category_id == Category.category_id, isouter=True).\
            filter((Product.name.like(search_query))|(Category.name.like(search_query)))
    all_products = search_results_query.paginate(per_page=12, page=page_num)
    total_products = len(search_results_query.all())
    return render_template('search_results.html', search_results = all_products, total_products = total_products)
    
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
