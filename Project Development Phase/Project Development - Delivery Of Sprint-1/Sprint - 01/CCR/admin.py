from flask import Blueprint, render_template

admin = Blueprint("admin", __name__)

@admin.route('/admin/tickets')
def tickets():
    return render_template('admin tickets.html', id = 0)

@admin.route('/admin/agents')
def agents():
    return render_template('admin agents.html', id = 1)

@admin.route('/admin/accept')
def accept():
    return render_template('admin acc agent.html', id = 2)

@admin.route('/admin/about')
def about():
    return render_template('admin about.html', id = 3)

@admin.route('/admin/support')
def support():
    return render_template('admin support.html', id = 4)
