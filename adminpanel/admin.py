from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from adminpanel.auth import login_required
from adminpanel.db import get_db

bp = Blueprint('admin', __name__)

@bp.route('/')
def index():
    db = get_db()
    if g.user is None:
        return redirect(url_for('auth.login'))
    else:
        users = db.execute(
            'SELECT id, username FROM users'
        ).fetchall()
        return render_template('home/index.html', users=users)


@bp.route('/delete', methods=('POST',))
@login_required
def delete():
    # reading the id to be deleted from request
    username = request.form['delete_user']
    # getting the db connection and 
    # deleting the user
    db = get_db()
    db.execute('DELETE FROM users WHERE username = ?', (username,))
    db.commit()
    return redirect(url_for('admin.index'))