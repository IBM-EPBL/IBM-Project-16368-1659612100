from flask import Blueprint, render_template, request, redirect, session, url_for
from flask_login import login_required, logout_user
import ibm_db
from .views import conn, customer
import uuid
from datetime import date, datetime

QUERY_STATUS_OPEN = "OPEN"
QUERY_STATUS_ASSIGNED_AGENT = "AGENT ASSIGNED"
QUERY_STATUS_CLOSE = "CLOSE"

cust = Blueprint("customer", __name__)

@cust.route('/customer/')
@login_required
def profile():
    '''
        Custome can see his/her profile card
    '''
    from .views import customer
        
    if hasattr(customer, 'uuid'):
        return render_template('cust profile.html', customer = customer, id = 0)

    else:
        return redirect(url_for('blue_print.logout'))

@cust.route('/customer/new', methods = ['GET', 'POST'])
@login_required
def new():
    '''
        Customer can create a new ticket 
    '''
    if request.method == 'POST':
        # collecting the query entered by the customer in the textarea
        query = request.form.get('query-box')

        msg = ""
        to_show = False

        if(len(query) == 0):
            msg = "Query cannot be empty!"
            to_show = True

        else:
            # updating the query in the database
            update_query = '''
                INSERT INTO tickets (ticket_id, raised_by, raised_on, issue, query_status)
                    VALUES (?, ?, ?, ?, ?)
            '''

            try:
                stmt = ibm_db.prepare(conn, update_query)

                # creating a uuid for the ticket_id
                ticket_id = str(uuid.uuid4())
                raised_by = customer.uuid
                raied_on = datetime.now()

                ibm_db.bind_param(stmt, 1, ticket_id)
                ibm_db.bind_param(stmt, 2, raised_by)
                ibm_db.bind_param(stmt, 3, raied_on)
                ibm_db.bind_param(stmt, 4, query)
                ibm_db.bind_param(stmt, 5, QUERY_STATUS_OPEN)

                ibm_db.execute(stmt)

                msg = "Ticket created!"
                to_show = True

            except:
                msg = "Something went wrong!"
                to_show = True

        return render_template('cust new ticket.html', id = 1, to_show = to_show, message = msg)

    return render_template('cust new ticket.html', id = 1)

@cust.route('/customer/tickets')
@login_required
def tickets():
    '''
        Fetching all the tickets raised by the customer
    '''

    fetch_query = '''
        SELECT  
            tickets.ticket_id,
            tickets.raised_on,
            tickets.query_status,
            agent.first_name, 
            tickets.issue
        FROM
            tickets
        LEFT JOIN 
            agent ON agent.agent_id = tickets.assigned_to AND
                tickets.raised_by = ? ORDER BY tickets.raised_on DESC
    '''

    # I am using the LEFT JOIN because
        # the customer should see both the assigned and unassigned tickets
    
    # Left side table - Tickets
    # Right side table - Agent

    # So all the tickets of the customer gets loaded (all the things in left table)
        # and the agents on the side

    from .views import customer
    raised_by = customer.uuid

    try:
        stmt = ibm_db.prepare(conn, fetch_query)
        ibm_db.bind_param(stmt, 1, raised_by)
        ibm_db.execute(stmt)

        tickets = ibm_db.fetch_assoc(stmt)
        tickets_list = []

        if tickets:
            # means, the customer has raised some tickets before
            while tickets != False:
                temp = []

                temp.append(tickets['TICKET_ID'])
                temp.append(str(tickets['RAISED_ON'])[0:10])
                temp.append(tickets['QUERY_STATUS'])
                temp.append(tickets['ISSUE'])
                temp.append(tickets['FIRST_NAME'])

                print(temp)

                tickets_list.append(temp)

                tickets = ibm_db.fetch_assoc(stmt)

            return render_template(
                'cust tickets.html',
                id = 2,
                tickets_to_show = True,
                tickets = tickets_list,
                msg = "These are your tickets"
            )

        else:
            # means, the customer is yet to raise a ticket
            return render_template(
                'cust tickets.html',
                id = 2,
                tickets_to_show = False,
                msg = "You are uet to rise a ticket"
            )

    except:
        # something fishy happened while loading the customer's tickets
        return render_template(
            'cust tickets.html',
            id = 2,
            to_show = True,
            message = "Something went wrong! Please Try Again"
        )

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
