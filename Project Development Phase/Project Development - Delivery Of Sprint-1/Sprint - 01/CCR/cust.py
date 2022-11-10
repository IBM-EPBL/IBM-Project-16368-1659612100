from flask import Blueprint, render_template, session
from flask_login import login_required

cust = Blueprint("customer", __name__)

@cust.route('/customer/')
@login_required
def profile():
    from .views import customer
        
    return render_template('cust profile.html', customer = customer, id = 0)

@cust.route('/customer/tickets')
@login_required
def tickets():
    return render_template('cust tickets.html', id = 1)

@cust.route('/customer/new')
@login_required
def new():
    return render_template('cust new ticket.html', id = 2)

@cust.route('/customer/change')
@login_required
def change():
    return render_template('cust change.html', id = 3)

@cust.route('/customer/about')
@login_required
def about():
    return render_template('cust about.html', id = 4)

@cust.route('/customer/support')
@login_required
def support():
    return render_template('cust support.html', id = 5)
