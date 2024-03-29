# This handles the login and registration for the wiki
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, escape
)
from werkzeug.security import check_password_hash, generate_password_hash

from fwiki.db import get_db

# All of our pages will have the prefix /auth/....
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = escape(request.form['email'])
        password = escape(request.form['password'])
        first = escape(request.form['first'])
        last = escape(request.form['last'])
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if not first:
            error = 'First name is required.'
        elif not last:
            error = 'Last name is required.'
        elif db.execute(
            'SELECT id FROM User WHERE email = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO User (email, password, first, last) VALUES (?, ?, ?, ?)',
                (username, generate_password_hash(password), first, last)
            )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = escape(request.form['email'])
        password = escape(request.form['password'])
        db = get_db()
        error = None
        user = db.execute(
            'SELECT id, email, password FROM User WHERE email =?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM User WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view