from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, escape
)
from werkzeug.exceptions import abort

from fwiki.auth import login_required
from fwiki.db import get_db

bp = Blueprint('fwiki', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT id, title, lastModified'
        ' FROM Entry'
        ' ORDER BY lastModified DESC'
    ).fetchall()
    return render_template('wiki-pages/index.html', posts=posts)


# This method returns the data on our selected entries
def get_entry(title, check_author=True):
    entry = get_db().execute(
        'SELECT * FROM Entry'
        ' INNER JOIN EntryData ON Entry.id = EntryData.entryNumber'
        ' WHERE Entry.title = ?',
        (title,)
    ).fetchall()

    if entry is None:
        abort(404, "Entry titled {0} doesn't exist.".format(id))

    # if check_author and entry['author_id'] != g.user['id']:
    #    abort(403)

    return entry


@bp.route('/<string:title>/getEntries', methods=('GET', 'POST'))
@login_required
def getEntry(title):
    entry = get_entry(title)
    entryInfo = []
    for e in entry:
        entryInfo.append(e['entryText'])
    print(entryInfo)

    entry = get_db().execute(
        'SELECT * FROM Entry'
        ' INNER JOIN EntryData ON Entry.id = EntryData.entryNumber'
        ' WHERE Entry.title = ?',
        (title,)
    ).fetchall()
    #if len(entry) == 0:
    #    abort(404, "There is no entry data.")
    entry = get_db().execute(
        'SELECT * FROM Entry'
        ' WHERE Entry.title = ?',
        (title,)
    ).fetchall()
    return render_template('wiki-pages/entry.html', entry=entry[0], info=entryInfo)


# TODO: This will be where our entries can be updated
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    entry = get_entry(id)

    if request.method == 'POST':
        title = escape(request.form['title'])
        # body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
             db = get_db()
             db.execute(
                 'UPDATE Entry SET title = ? WHERE id = ?',
                 (title, id)
             )
             db.commit()
             # TODO: for calvin, not sure what to return
             # return redirect(url_for('wiki.index'))

    return render_template('wiki/update.html', entry=entry)


@bp.route('/changeReadTo', methods=('GET', 'POST'))
@login_required
def changeReadTo():
    abort(404, "There is no entry data.")

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')