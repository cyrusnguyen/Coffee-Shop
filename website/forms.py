import email
from sre_constants import MAX_UNTIL
from sys import maxsize
from unittest.util import _MAX_LENGTH
from flask_wtf.file import FileRequired, FileField, FileAllowed
from xml.etree.ElementTree import Comment
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, FileField, RadioField, DateField, TimeField
from wtforms.validators import InputRequired, Email,  EqualTo
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from .models import Category

ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}


# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")


# this is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           Email("Please enter a valid email")])
    phone_number = StringField("Phone number", validators=[InputRequired()]) 
    address = StringField("Address", validators=[InputRequired()])                        
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")


# Contact us Form
class ContactUsForm(FlaskForm):
    user_name = StringField("Name", validators=[InputRequired()], render_kw={"style": "font-weight: bold; color: white;"})
    email = StringField("Email Address", validators=[
                           Email("Please enter a valid email")], render_kw={"style": "font-weight: bold; color: white;"})
    subject = StringField('Subject', validators=[InputRequired()], render_kw={"style": "font-weight: bold; color: white;"})
    message = TextAreaField('Message', validators=[InputRequired()], render_kw={"style": "font-weight: bold; color: white;"})
    submit = SubmitField("Send")


# Product Creation Form
class BasicInfoForm(FlaskForm):
    def get_all_categories():
        result = list()
        return result
    
    product_name = StringField("Product Name", validators=[InputRequired()])
    
    price = StringField("Price", validators=[InputRequired()])
    number_of_products = IntegerField("Number of products in stock: ", validators=[InputRequired()])
    choose_file = FileField("Upload File", validators=[FileRequired(message='Please upload product image'),
                                                       FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    # category = RadioField("Category", choices=[(categories.category_id, categories.name) for categories in Category.query.all()], validators=[InputRequired()])
    status = RadioField("Status", choices=['Available','Sold Out'], validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    country = StringField("Country", validators=[InputRequired()])
    zipcode = StringField("ZipCode", validators=[InputRequired()])
    created_at = TimeField("Start Time", validators=[InputRequired()])
    submit = SubmitField("Create")

# Product Update Form
class UpdateInfoForm(FlaskForm):
    product_name = StringField("Product Name", validators=[InputRequired()])
    
    price = StringField("Price", validators=[InputRequired()])
    number_of_products = IntegerField("Number of products: ", validators=[InputRequired()])
    choose_file = FileField("Upload File", validators=[FileRequired(message='Image cannot be empty'),
                                                       FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    d_style = RadioField("Dance Style", choices=[
                         'Salsa', 'Bachata', 'Zouk', 'Kizumba'], validators=[InputRequired()])
    producer = StringField("Producer", validators=[InputRequired()])
    status = RadioField("Status", choices=[
        'Upcoming', 'Cancelled', 'Sold Out', 'Inactive', 'Unpublished'], validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    country = StringField("Country", validators=[InputRequired()])
    zipcode = StringField("ZipCode", validators=[InputRequired()])
    s_time = TimeField("Start Time", validators=[InputRequired()])
    e_time = TimeField("End Time", validators=[InputRequired()])
    s_date = DateField("Start Date", validators=[InputRequired()])
    e_date = DateField("End Date", validators=[InputRequired()])
    submit = SubmitField("Update")


# Product Delete Form
class DeleteInfoForm(FlaskForm):
    submit = SubmitField("Delete")
    

# Comment Form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Create')

# Purchase product form
class PurchaseTicketForm(FlaskForm):
    productNo = IntegerField('Amount of products', [ validators.InputRequired()])
    submit = SubmitField("Purchase")
    

# Update form
class Updateform(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           Email("Please enter a valid email")])
    phone_number = StringField("Phone number", validators=[InputRequired()]) 

    address = StringField("Address", validators=[InputRequired()])  
                  

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Update")