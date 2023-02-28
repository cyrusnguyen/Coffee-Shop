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
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           Email("Please enter a valid email")])
    subject = StringField('Subject', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField("Create")


# Event Creation Form
class BasicInfoForm(FlaskForm):
    event_name = StringField("Event Name", validators=[InputRequired()])
    
    price = StringField("Price", validators=[InputRequired()])
    number_of_tickets = IntegerField("Number of tickets: ", validators=[InputRequired()])
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
    submit = SubmitField("Create")

# Event Update Form
class UpdateInfoForm(FlaskForm):
    event_name = StringField("Event Name", validators=[InputRequired()])
    
    price = StringField("Price", validators=[InputRequired()])
    number_of_tickets = IntegerField("Number of tickets: ", validators=[InputRequired()])
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


    # Event Delete Form####
class DeleteInfoForm(FlaskForm):
    submit = SubmitField("Delete")
    

# comment Form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Create')

# Purchase ticket form
class PurchaseTicketForm(FlaskForm):
    ticketNo = IntegerField('Amount of tickets', [ validators.InputRequired()])
    submit = SubmitField("Purchase")
    

# this is the registration form
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