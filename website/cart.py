from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, session
from .models import Product, User, Cart, CartProduct
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import db, app
import os


cartbp = Blueprint('cart', __name__)

@cartbp.route('/add-to-cart/<id>', methods=['GET', 'POST'])
def add_to_cart(id):
    
    
    product_obj = Product.query.filter_by(product_id=id).first()
    product_list = list()

    
    # If there's already a cart, check if item is in cart
    if session.get('session_shopping_cart'):
        product_list = session['session_shopping_cart']['Shopping_cart']

    if request.method == "POST":
        product_quantity = int(request.form.get("product_quantity"))
        session.pop('session_shopping_cart', None)

        isExists = False
        for product in product_list:
            # Add quantity if exists
            if product['product_id'] == id:
                product['quantity'] += product_quantity
                product['total'] = product_obj.price * product['quantity']
                product['modified_at'] = datetime.now()
                isExists = True
        if not isExists:
            product_dict = {
                "product_dict": product_obj.as_dict(),
                "product_id": id,
                "quantity": product_quantity,
                "created_at": datetime.now(),
                "modified_at": None,
                "total": product_obj.price * product_quantity
            }
            product_list.append(product_dict)
        session['session_shopping_cart'] = {"Shopping_cart": product_list}
        session['session_shopping_cart']['cart_total'] = get_cart_price(session['session_shopping_cart']['Shopping_cart'])
        session['session_shopping_cart']['cart_quantity'] = get_cart_quantity(session['session_shopping_cart']['Shopping_cart'])
    return redirect(request.referrer)

def get_cart_price(cart_items):
    cart_price = 0
    for item in cart_items:
        cart_price += float(item['total'])
    return cart_price

def get_cart_quantity(cart_items):
    cart_quantity = 0
    for item in cart_items:
        cart_quantity += int(item['quantity'])
    return int(cart_quantity)

@cartbp.route('/update-cart', methods=['GET', 'POST'])
def update_cart():

    product_list = session['session_shopping_cart']['Shopping_cart']

    if request.method == "POST":
        new_product_list = []
        session.pop('session_GioHang', None)

        for product in product_list:
            quantity_input = int(request.form.get('product_quantity' + str(product['product_id'])))
            product['quantity'] = quantity_input
            product['total'] = product['product_dict']['price'] * product['quantity']
            product['modified_at'] = datetime.now()
            new_product_list.append(product)

        session['session_shopping_cart'] = {"Shopping_cart": new_product_list}
        session['session_shopping_cart']['cart_total'] = get_cart_price(session['session_shopping_cart']['Shopping_cart'])
        session['session_shopping_cart']['cart_quantity'] = get_cart_quantity(session['session_shopping_cart']['Shopping_cart'])

    return redirect(request.referrer)



@cartbp.route('/remove-from-cart', methods=['GET', 'POST'])
def remove_from_cart():

    product_list = session['session_shopping_cart']['Shopping_cart']

    if request.method == "POST":
        id = request.form.get('product_id_remove')
        session.pop('session_shopping_cart', None)
        new_product_list = [item for item in product_list if item['product_id']!=id]
        session['session_shopping_cart'] = {"Shopping_cart": new_product_list}
        session['session_shopping_cart']['cart_total'] = get_cart_price(session['session_shopping_cart']['Shopping_cart'])
        session['session_shopping_cart']['cart_quantity'] = get_cart_quantity(session['session_shopping_cart']['Shopping_cart'])
    return redirect(request.referrer)


@cartbp.route('/view-cart', methods=['GET', 'POST'])
def view_cart():


    return render_template('cart.html')

# @cartbp.route('/view-cart/<id>', methods=['GET', 'POST'])
# def confirm_cart(id):
    
#     product_id = Product.query.filter_by(comment_id=id).first().products.product_id  
#     if request.method == "POST":
#         # comment_id = request.form.get("comment_id")
        
#         print('Successfully delete comment', 'success')
#     return redirect(url_for('product.show', id=product_id))

@cartbp.route('/delete-cart')
def delete_cart():
    print("Deleting cart:", session['session_shopping_cart'])
    session.pop('session_shopping_cart', None)
    return redirect(url_for('main.index'))


