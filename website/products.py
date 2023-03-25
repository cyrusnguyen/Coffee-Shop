from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, session
from .models import Product, Comment, User, Cart
from website.forms import CommentForm, ContactUsForm, BasicInfoForm, PurchaseProductForm, DeleteInfoForm
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import db, app
import os
from werkzeug.utils import secure_filename



# Use of blue print to group routes,
# name - first argument is the blue print name
# import name - second argument - helps identify the root url for it
productbp = Blueprint('product', __name__)


@productbp.route('/product/<id>', methods=['GET', 'POST'])
def show(id):
    SQLdetails = Product.query.filter_by(product_id=id).first()
    # if there is no user with that name
    if SQLdetails is None:
        return render_template("404.html")
    user_information = None
    if current_user.is_authenticated:
        if SQLdetails.status == "Unpublished":
            if current_user.user_id != SQLdetails.user_id :
                return render_template("404.html")
                
            
        user_information = User.query.filter_by(user_id=current_user.user_id).first()


    comm_form = CommentForm()
    productForm = PurchaseProductForm()

    return render_template('view.html', product = SQLdetails, user = user_information, form = comm_form, productForm = productForm)

@productbp.route('/cart/<id>', methods=['GET', 'POST'])
@login_required
def show_cart(id):
    cart_details = Cart.query.filter_by(user_id=id).first()
    
    return render_template('cart.html', cart=cart_details)


@productbp.route('/create-product', methods=['GET', 'POST'])
@login_required
def create_product():
    bi_form = BasicInfoForm()
    if bi_form.validate_on_submit():
        upload_file = check_upload_file(bi_form)
        
        new_product = Product(
            name = bi_form.product_name.data,
            description = bi_form.description.data,
            image = upload_file,
            price = bi_form.price.data,
            quantity = bi_form.number_of_products.data,
            category_id = int(bi_form.category.data),
            status = bi_form.status.data,

        )
        db.session.add(new_product)

        db.session.commit()
        

        return redirect(url_for('main.show_products'))
    return render_template('create_product.html', form=bi_form)

def check_upload_file(form):
  #get file data from form  
  fp = form.choose_file.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/img/products',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path



###Update product form







@productbp.route('/update-product/<id>', methods=['GET', 'POST'])
@login_required
def update_product(id):

    SQLdetails = Product.query.filter_by(product_id=id).first()
    user_information = User.query.filter_by(user_id=current_user.user_id).first()

    if current_user.role.lower() == "admin":


        # print('Method type: ', request.method)
        bi_form = BasicInfoForm()
        
        if bi_form.validate_on_submit():
            upload_file = check_upload_file(bi_form)
            
            update = Product.query.filter_by(product_id = id).update(dict(
            name = bi_form.product_name.data,
            description = bi_form.description.data,
            image = upload_file,
            price = bi_form.price.data,
            status = bi_form.status.data,
            # category_id = bi_form.category.data,
            quantity = bi_form.number_of_products.data
            ))

            db.session.commit()
            

            return redirect(url_for('main.show_products'))
        return render_template('update_product.html', form=bi_form, product = SQLdetails, user = user_information)
        
    else:
        return render_template("404.html")


@productbp.route('/delete-product/<id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):

       

    SQLdetails = Product.query.filter_by(product_id=id).first()
    user_information = User.query.filter_by(user_id=current_user.user_id).first()

    if current_user.role.lower() == "admin":

        bi_form = DeleteInfoForm()
        
        if bi_form.validate_on_submit():
           
            
            

            Product.query.filter_by(product_id = id).delete()
            db.session.commit()
            

            return redirect(url_for('main.show_products', id = '1'))
        return render_template('delete_product.html', form=bi_form, product = SQLdetails,user = user_information)
        
    else:
           return render_template("404.html")









           

@productbp.route('/product/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    comm_form = CommentForm()
    product_obj = Product.query.filter_by(product_id=id).first()  
    if comm_form.validate_on_submit():
        #read the comment from the form
        comment = Comment(
            text=comm_form.text.data,  
            products=product_obj,
            users=current_user) 

        db.session.add(comment) 
        db.session.commit() 
    return redirect(url_for('product.show', id=id))

@productbp.route('/<id>/delete-comment', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    if current_user.role.lower() == "admin":
        product_id = Comment.query.filter_by(comment_id=id).first().products.product_id  
        if request.method == "POST":
            # comment_id = request.form.get("comment_id")
            
            Comment.query.filter_by(comment_id=id).delete()

            db.session.commit() 
        return redirect(url_for('product.show', id=product_id))
    return redirect(url_for('product.show', id=product_id))
    
