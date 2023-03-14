from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request
from .models import Product, Comment, User, Cart
from website.forms import CommentForm, ContactUsForm, BasicInfoForm, PurchaseTicketForm, DeleteInfoForm
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import db, app
import os
from werkzeug.utils import secure_filename



# Use of blue print to group routes,
# name - first argument is the blue print name
# import name - second argument - helps identify the root url for it
productbp = Blueprint('product', __name__, url_prefix='/products')


@productbp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    SQLdetails = Product.query.filter_by(product_id=id).first()
    # if there is no user with that name
    if SQLdetails is None:
        return render_template("404.html")
    user_information = 0
    if current_user.is_authenticated:
        if SQLdetails.status == "Unpublished":
            if current_user.id != SQLdetails.user_id :
                return render_template("404.html")
                
            
        user_information = User.query.filter_by(id=current_user.id).first()


    comm_form = CommentForm()
    productForm = PurchaseTicketForm()
    #if productForm.productNo.data == 
   ## print(SQLdetails.id)##
    print('Method type: ', request.method)
    if productForm.validate_on_submit():
        #read the product amount from the form
        PurchasedTicketInfo = Cart(
                        amount = productForm.productNo.data,
                        user = current_user,
                        product = SQLdetails)
        db.session.add(PurchasedTicketInfo) 
        db.session.commit() 
        print('Successfully sent message', 'success')

    
    
    return render_template('view.html', product=SQLdetails, user = user_information, form=comm_form, TicketFrom = productForm)


@productbp.route('/create-product', methods=['GET', 'POST'])
@login_required
def create_product():
    print('Method type: ', request.method)
    bi_form = BasicInfoForm()
    
    if bi_form.validate_on_submit():
        upload_file = check_upload_file(bi_form)
        new_product = Product(name = bi_form.product_name.data,
        description = bi_form.description.data,
        image = upload_file,
        price = bi_form.price.data,
        date_start = bi_form.s_date.data,
        date_end = bi_form.e_date.data,
        time_start = bi_form.s_time.data,
        time_end = bi_form.e_time.data,
        producer = bi_form.producer.data,
        status = bi_form.status.data,
        style = bi_form.d_style.data,
        productNo = bi_form.number_of_products.data,
        address = bi_form.address.data + ", " + bi_form.zipcode.data,
        city = bi_form.city.data,
        country = bi_form.country.data,
        
        user = current_user
        )
        db.session.add(new_product)

        db.session.commit()
        print('Successfully sent message', 'success')
        

        return redirect(url_for('main.show_all', id = '1'))
    return render_template('create_product.html', form=bi_form)

def check_upload_file(form):
  #get file data from form  
  fp = form.choose_file.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/img/product',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path



###Update product form







@productbp.route('/update-product', methods=['GET', 'POST'])
@login_required
def update_product():

    SQLdetails = Product.query.filter_by(id=idstorage).first()
    user_information = User.query.filter_by(id=current_user.id).first()

    if SQLdetails.user_id == current_user.id:


        print('Method type: ', request.method)
        bi_form = BasicInfoForm()
        
        if bi_form.validate_on_submit():
            upload_file = check_upload_file(bi_form)
            
            
            print(bi_form.category.data)
            update = Product.query.filter_by(id = idstorage).update(dict(name = bi_form.product_name.data,
            description = bi_form.description.data,
            image = upload_file,
            price = bi_form.price.data,
            status = bi_form.status.data,
            # category_id = bi_form.category.data,
            quantity = bi_form.number_of_products.data))

            db.session.commit()
            print('Successfully sent message', 'success')
            

            return redirect(url_for('main.show_all', id = '1'))
        return render_template('update_product.html', form=bi_form, product = SQLdetails,user = user_information)
        
    else:
           return render_template("404.html")


@productbp.route('/delete-product', methods=['GET', 'POST'])
@login_required
def delete_product():

       

    SQLdetails = Product.query.filter_by(id=idstorage).first()
    user_information = User.query.filter_by(id=current_user.id).first()

    if SQLdetails.user_id == current_user.id:


        print('Method type: ', request.method)
        bi_form = DeleteInfoForm()
        
        if bi_form.validate_on_submit():
           
            
            

            Product.query.filter_by(id = idstorage).delete()
            db.session.commit()
            print('Successfully sent message', 'success')
            

            return redirect(url_for('main.show_all', id = '1'))
        return render_template('delete_product.html', form=bi_form, product = SQLdetails,user = user_information)
        
    else:
           return render_template("404.html")









           

@productbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    comm_form = CommentForm()
    product_obj = Product.query.filter_by(id=id).first()  
    if comm_form.validate_on_submit():
        #read the comment from the form
        comment = Comment(text=comm_form.text.data,  
                        product=product_obj,
                        user=current_user) 
        #here the back-referencing works - comment.destination is set
        # and the link is created
        db.session.add(comment) 
        db.session.commit() 
        print('Successfully sent message', 'success')
    return redirect(url_for('product.show', id=id))
