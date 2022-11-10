from flask import Blueprint, render_template, request, redirect, session, url_for
import hashlib
import re
from flask_login import login_required, login_user, logout_user
import ibm_db
import uuid
from datetime import date
from .model import Customer

views = Blueprint("blue_print", __name__)
email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
pass_regex = r"^[A-Za-z0-9_-]*$"

customer = Customer()

conn = ibm_db.connect('DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tdn81266;PWD=7LY8okjAouJf3LoO', '', '')

@views.route('/logout')
@login_required
def logout():
    session.pop('LOGGED_IN_AS')
    logout_user()

    return redirect(url_for('blue_print.login'))

@views.route('/', methods = ['GET', 'POST'])
def login():
    # if method is POST
    if request.method == 'POST':
        # getting the data entered by the user 
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role-check')

        msg = ""
        to_show = False

        # validating the inputs entered by the user
        if(not (re.fullmatch(email_regex, email))):
            msg = "Enter a valid email"
            to_show = True

        elif (len(password) < 8):
            msg = "Password must be atleast 8 characters long!"
            to_show = True

        # Admin login
        if email == "admin.ccr@gmail.com":
            if password == "admin.ccr@2022":
                return redirect('/admin/tickets')

            else:
                to_show = True
                password = ""
                msg = "Invalid password!"

        # Customer or Agent
        else:
            if to_show:
                # there is something fishy with the user's inputs
                password = ""

            elif (not to_show):
                # the user's inputs are valid
                # checking if the login credentials are valid
                if role == "Customer":
                    # checking if the entry of the mail entered is present in the database
                    mail_check_query = "SELECT * FROM customer WHERE email = ?"
                    stmt = ibm_db.prepare(conn, mail_check_query)
                    ibm_db.bind_param(stmt, 1, email)
                    ibm_db.execute(stmt)

                    account = ibm_db.fetch_assoc(stmt)

                    if account:
                        # valid customer
                        # i.e, mail is present in the database

                        # checking if the customer entered a valid password now
                        # encrypting the entered password
                        passcode = str(hashlib.sha256(password.encode()).hexdigest())

                        # now checking if the encrypted string is same as that of the one in database
                        if (account['PASSCODE'] == passcode):
                            msg = "Valid Login"
                            to_show = True

                            # creating a customer object
                            customer.set(
                                account['CUST_ID'],
                                account['FIRST_NAME'],
                                account['LAST_NAME'],
                                account['EMAIL'],
                                account['PASSCODE'],
                                account['DATE_JOINED']
                            )

                            session.permanent = False
                            session['LOGGED_IN_AS'] = "CUSTOMER"
                            login_user(customer, remember=True)

                            return redirect('/customer/')

                        else:
                            # customer entered invalid password
                            msg = "Invalid password"
                            password = ""
                            to_show = True

                    else:
                        # invalid customer
                        # i.e, entered mail is not present in the database
                        msg = "User does not exist"
                        email = ""
                        password = ""
                        to_show = True

                else:
                    # user is an Agent
                    print("hello")

        return render_template(
            'login.html',
            to_show = to_show,
            message = msg,
            email = email,
            password = password
        )

    return render_template('login.html')

@views.route('/register', methods = ['GET', 'POST'])
def register():
    # if method is POST
    if request.method == 'POST':
        # getting all the data entered by the user
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role-check')

        msg = ""
        to_show = False

        # validating the inputs 
        if len(first_name) < 2:
            msg = "First Name must be atleast 5 characters long!"
            to_show = True

        elif len(last_name) < 2:
            msg = "Last Name must be atleast 5 characters long!"
            to_show = True

        elif(not (re.fullmatch(email_regex, email))):
            msg = "Please enter valid email"
            to_show = True

        elif((len(password) < 8) or (len(confirm_password) < 8)):
            msg = "Password must be atleast 8 characters long!"
            to_show = True

        elif (password != confirm_password):
            msg = "Passwords do not match"
            to_show = True

        elif (not (re.fullmatch(pass_regex, password))):
            msg = "Enter valid password"
            to_show = True

        if to_show:
            # there is something fishy with the inputs
            password = confirm_password = ""

        # by here the inputs are validated, because to_show is False
        # registering the user / agent with the database
        elif (not to_show):
            if role == "Customer":
                # the user is a Customer
                # checking whether the user with the same email already there
                check_mail_query = "SELECT * FROM customer WHERE email = ?"
                stmt = ibm_db.prepare(conn, check_mail_query)
                ibm_db.bind_param(stmt, 1, email)
                ibm_db.execute(stmt)

                account = ibm_db.fetch_assoc(stmt)

                if account:
                    # user already exists
                    msg = "Email already exists!"
                    to_show = True

                else:
                    # new customer
                    # adding the customer details to the detabase
                    user_insert_query ='''INSERT INTO customer
                            (cust_id, first_name, last_name, email, passcode, date_joined) 
                            VALUES (?, ?, ?, ?, ?, ?)'''

                    # creating a UUID for the customer
                    user_uuid = str(uuid.uuid4())

                    # encrypting the customer's password using SHA-256
                    passcode = str(hashlib.sha256(password.encode()).hexdigest())
                    date_joined = date.today()

                    stmt = ibm_db.prepare(conn, user_insert_query)
                    ibm_db.bind_param(stmt, 1, user_uuid)
                    ibm_db.bind_param(stmt, 2, first_name)
                    ibm_db.bind_param(stmt, 3, last_name)
                    ibm_db.bind_param(stmt, 4, email)
                    ibm_db.bind_param(stmt, 5, passcode)
                    ibm_db.bind_param(stmt, 6, date_joined)

                    ibm_db.execute(stmt)

                    # redirecting the customer to the login page
                    msg = "Account created. Please Login!"
                    to_show = True

                    return render_template('login.html', message = msg, to_show = to_show)
                
            else:
                # the role is Agent
                # can be done in Sprint 2/3
                print("Sprint 2/3")

        return render_template(
            'register.html',
            to_show = to_show,
            message = msg,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
            confirm_password = confirm_password,
            role = role
        )
    
    return render_template('register.html')
