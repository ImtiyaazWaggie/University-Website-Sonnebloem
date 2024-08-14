import functools
import random

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def generate_admin_username():
    return f"ADMIN{random.randint(100000, 999999)}"

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        error = None

        if not first_name:
            error = 'First Name is required.'
        elif not last_name:
            error = 'Last Name is required.'
        if not phone_number:
            error = 'Phone Number is required.'
        elif not email:
            error = 'Email is required.'
        if not password:
            error = 'Password is required.'

        if error is not None:
            flash(error)
        else:
            username = generate_admin_username()    
            try:
                db.execute(
                    "INSERT INTO users (username, first_name, last_name, phone_number, email, password) VALUES (?, ?, ?, ?, ?, ?)",
                    (username, first_name, last_name, phone_number, email, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

    return render_template('auth/register.html')



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('university.admin_dashoard'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('university.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view       