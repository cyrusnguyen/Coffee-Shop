from datetime import datetime
from flask import Blueprint, Markup, render_template, flash, redirect, url_for, request, session
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
        isFlash = False
        for product in product_list:
            # Add quantity if exists
            if product['product_id'] == id:
                if product_quantity <= product['product_dict']['quantity'] and product_quantity+product['quantity'] <= product['product_dict']['quantity']:
                    product['quantity'] += product_quantity
                    product['total'] = product_obj.price * product['quantity']
                    product['modified_at'] = datetime.now()
                    isExists = True
                else:
                    session['session_shopping_cart'] = {"Shopping_cart": product_list}
                    session['session_shopping_cart']['cart_total'] = get_cart_price(session['session_shopping_cart']['Shopping_cart'])
                    session['session_shopping_cart']['cart_quantity'] = get_cart_quantity(session['session_shopping_cart']['Shopping_cart'])
                    flash("Error! Only {0} products in stock".format(product['product_dict']['quantity']), 'error')
                    isExists = True
                    isFlash = True 
        if not isExists:
            if product_quantity <= product_obj.quantity:
                product_dict = {
                    "product_dict": product_obj.as_dict(),
                    "product_id": id,
                    "quantity": product_quantity,
                    "created_at": datetime.now(),
                    "modified_at": None,
                    "total": product_obj.price * product_quantity
                }
                product_list.append(product_dict)
            else:
                session['session_shopping_cart'] = {"Shopping_cart": product_list}
                session['session_shopping_cart']['cart_total'] = get_cart_price(session['session_shopping_cart']['Shopping_cart'])
                session['session_shopping_cart']['cart_quantity'] = get_cart_quantity(session['session_shopping_cart']['Shopping_cart'])
                flash("Error! Only {0} products in stock".format(product_obj.quantity), 'error')
                isFlash = True 
        session['session_shopping_cart'] = {"Shopping_cart": product_list}
        session['session_shopping_cart']['cart_total'] = get_cart_price(session['session_shopping_cart']['Shopping_cart'])
        session['session_shopping_cart']['cart_quantity'] = get_cart_quantity(session['session_shopping_cart']['Shopping_cart'])
        if isFlash == False and session.get('_flashes') != None: 
            session['_flashes'].clear()
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

    product_list = session['session_shopping_cart']['Shopping_cart'] if session.get('session_shopping_cart') else []

    if request.method == "POST":
        new_product_list = []
        session.pop('session_GioHang', None)

        for product in product_list:
            quantity_input = int(request.form.get('product_quantity' + str(product['product_id'])))
            if quantity_input <= int(product['product_dict']['quantity']):
                product['quantity'] = quantity_input
                product['total'] = product['product_dict']['price'] * product['quantity']
                product['modified_at'] = datetime.now()
                new_product_list.append(product)
            else: 
                session['session_shopping_cart'] = {"Shopping_cart": product_list}
                session['session_shopping_cart']['cart_total'] = get_cart_price(session['session_shopping_cart']['Shopping_cart'])
                session['session_shopping_cart']['cart_quantity'] = get_cart_quantity(session['session_shopping_cart']['Shopping_cart'])
                return render_template('cart.html', Message="There's not enough stock. Remaining products for {0}: {1}".format(product['product_dict']['name'],product['product_dict']['quantity']))

        session['session_shopping_cart'] = {"Shopping_cart": new_product_list}
        session['session_shopping_cart']['cart_total'] = get_cart_price(session['session_shopping_cart']['Shopping_cart'])
        session['session_shopping_cart']['cart_quantity'] = get_cart_quantity(session['session_shopping_cart']['Shopping_cart'])

    return render_template('cart.html')



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
    
    user_carts = Cart.query.filter_by(user_id=current_user.user_id).all()
    for cart in user_carts:
        for product in cart.cart_products:
            print(product.cart_product_id)
        print("")
    
    return render_template('cart.html')


@cartbp.route('/purchase', methods=['GET', 'POST'])
def purchase(): 
    if session.get('session_shopping_cart'):
        product_list = session['session_shopping_cart']['Shopping_cart']
        if request.method == "POST":
            new_cart = Cart(
                user_id = current_user.user_id,
                subtotal = session['session_shopping_cart']['cart_total'],
                total_quantity = session['session_shopping_cart']['cart_quantity'],
                delivery_address = str(request.form.get('uaddress')),
                email = request.form.get('uemail'),
                phoneNo = request.form.get('uphone')
            )
            for product in product_list:
                new_cart_product = CartProduct(
                    quantity = product['quantity'],
                    total = product['total'],
                    created_at = product['created_at'],
                    modified_at = product['modified_at'],
                    carts = new_cart,
                    product_id = product['product_dict']['product_id'],
                    name = product['product_dict']['name'],
                    price = product['product_dict']['price']
                )
                remaining_products = product['product_dict']['quantity'] -  product['quantity']
                new_sold_quantity = product['product_dict']['sold_quantity'] + product['quantity']
                if remaining_products < 1:
                    db.session.query(Product).filter_by(product_id = product['product_dict']['product_id']).update(dict(
                        quantity = remaining_products,
                        sold_quantity = new_sold_quantity,
                        status = "Sold Out"
                    ))
                else:
                    db.session.query(Product).filter_by(product_id = product['product_dict']['product_id']).update(dict(
                            quantity = remaining_products,
                            sold_quantity = new_sold_quantity
                        ))
                db.session.add(new_cart_product)
            db.session.commit()
            session.pop('session_shopping_cart', None)

            home_url = url_for('main.index')
            success_message = '''<div class="container">
            <h1>We have receive your order!</h1>
            <p>Thanks for supporting us. We will send you an email for the confirmation.</p>
            <p>Click <a href="{0}">Here</a> to go back to Home Page </p>
            </div>'''.format(home_url)
            return render_template('blank.html', Message = Markup(success_message))
        return render_template('purchase.html')
    else:
        show_all_url = url_for('main.show_products')
        error_message = '''<div class="container">
        <h1>You dont have any products in your cart!</h1>
        <p>Please <a href="{0}">add more products here</a> to continue. </p>
        <p>Thank you!</p>
        </div>'''.format(show_all_url)
        return render_template('blank.html', Message = Markup(error_message))

@cartbp.route('/delete-cart')
def delete_cart():
    # print("Deleting cart:", session['session_shopping_cart'])
    session.pop('session_shopping_cart', None)
    return redirect(url_for('main.index'))


