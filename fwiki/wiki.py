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
    userReadTo = get_db().execute(
        'SELECT chapterNumber, book '
        'FROM ReadTo WHERE user = ?',
        (g.user['id'],)
    ).fetchall()
    for e in entry:
        canAddOutside = True
        for rt in userReadTo:
            if rt['book'] == e['bookId']:
                canAddOutside = False
                if int(rt['chapterNumber']) <= int(e['chapterNumber']):
                    entryInfo.append(e['entryText'])
        if canAddOutside:
            entryInfo.append(e['entryText'])
    print(entryInfo)
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
    entry = get_db().execute(
        'SELECT * FROM Entry'
        ' WHERE Entry.id = ?',
        (id,)
    ).fetchone()
    if request.method == 'POST':
        bookTitle = escape(request.form['bookTitle'])
        entryText = request.form['entryText']
        chapterNumber = request.form['chapterNumber']
        error = None

        if not bookTitle:
            error = 'Title is required.'
        elif not entryText:
            error = 'Entry text is required.'
        elif not chapterNumber and int(chapterNumber) > 0:
            error = 'Chapter number requires a valid int input.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            # First check if book already exists, if not add it
            bookId = db.execute(
                'SELECT id FROM Book WHERE name = ?', (bookTitle,)
            ).fetchone()
            if len(bookId) == 0:
                db.execute(
                    'INSERT INTO Book (name) VALUES (?)',
                    (bookTitle,)
                )
                db.commit()
                bookId = db.execute(
                    'SELECT id FROM Book WHERE name = ?',
                    (bookTitle,)
                ).fetchone()['id']
            db.execute(
                'INSERT INTO EntryData (entryText, modified, entryNumber, chapterNumber, bookId) '
                'VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?)',
                (entryText, id, chapterNumber, bookId)
            )
            db.commit()
            return redirect(url_for('fwiki.index'))

    return render_template('wiki-pages/update.html', entry=entry)


@bp.route('/changeReadTo', methods=('GET', 'POST'))
@login_required
def changeReadTo():
    return render_template('wiki-pages/change.html')


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
            return redirect(url_for('fwiki.index'))

    return render_template('wiki-pages/change.html')


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM Entry WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('fwiki.index'))

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def deleteEntryData(entryText):
    db = get_db()
    db.execute('DELETE FROM EntryData WHERE entryText = ?', (entryText,))
    db.commit()
    return redirect(url_for('fwiki.index'))