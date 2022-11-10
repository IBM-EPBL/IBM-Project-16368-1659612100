from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

agent = Blueprint("agent", __name__)

@agent.route('/agent/no-show', methods = ['GET', 'POST'])
@login_required
def no_show():
    from .views import agent
    
    # extra-level security
    if hasattr(agent, 'first_name'):
        return render_template('agent no show.html', agent = agent)

    else:
        redirect(url_for('/'))
