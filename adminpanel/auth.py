import functools
from secure import SecureHeaders, SecureCookie
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from adminpanel.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    """ loading the user details if the user is logged"""
    user_id = session.get('user_id')

    if not user_id:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        if db.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} already exists.'

        if error is None:
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM users WHERE username = ? ', (username,)
        ).fetchone()

        # verifying the user and password
        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'
            flash(error)
        else:
            session.clear()
            session['user_id'] = user['id']
            # returning userid to verify login
            # TODO: replace userid with index page
            return user['id']

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# defining a decorator to check 
# if a user is logged in 
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))
        return view(**kwargs)
    
    return wrapped_view
