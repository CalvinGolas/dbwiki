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


# This will be where our entries can be updated
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    entry = get_db().execute(
        'SELECT * FROM Entry'
        ' WHERE Entry.id = ?',
        (id,)
    ).fetchone()
    if request.method == 'POST':
        print(request.form)
        bookTitle = request.form['bookTitle']
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
            ).fetchone()['id']
            if bookId is None:
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
                (entryText, id, chapterNumber, bookId,)
            )
            db.commit()
            return redirect(url_for('fwiki.index'))

    return render_template('wiki-pages/update.html', entry=entry)


def getBook():
    book = get_db().execute('SELECT name FROM Book ORDER BY Book.name').fetchall();
    bookEntry = []
    for e in book:
        bookEntry.append(e['name'])
    return bookEntry

@bp.route('/changeReadTo', methods=('GET', 'POST'))
@login_required
def changeReadTo():
    bookEntry = getBook()

    if request.method == 'POST':
        db = get_db()
        book = request.form.get('book')
        chapter = escape(request.form['chapter'])
        error = None
        num = get_book_id(book)

        if chapter is None:
            error = "Chapter is required."
        else:
            check = db.execute('SELECT ReadTo.book FROM'
                       '    ReadTo INNER JOIN Book ON Book.id = ReadTo.book'
                       '    WHERE Book.name = ? AND ReadTo.user = ?', (book, g.user['id'])).fetchone()
            if check is None:
                db.execute('INSERT INTO ReadTo'
                           '    (book, chapterNumber, user)'
                           '    VALUES'
                           '    (?, ?, ?)', (num, chapter, g.user['id']))
                db.commit()
            else:
                db.execute('UPDATE ReadTo'
                           '    SET chapterNumber=? '
                           '    WHERE book=? AND user = ?', (chapter, num, g.user['id']))
                db.commit()

    return render_template('wiki-pages/change.html', entry=bookEntry)

def get_book_id(title):
    db = get_db()
    num = db.execute('SELECT id FROM Book WHERE name = ?', (title,)).fetchone()['id']
    return num

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        entry = request.form['entry']
        error = None

        if not entry:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO Entry (title, lastModified)'
                ' VALUES (?, ?)',
                (title, CURRENT_TIMESTAMP)
            )
            db.commit()
            return redirect(url_for('fwiki.index'))

    return render_template('wiki-pages/newentry.html')


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM Entry WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('fwiki.index'))

@bp.route('/<string:entryText>/deleteEntryData', methods=('POST',))
@login_required
def deleteEntryData(entryText):
    db = get_db()
    db.execute('DELETE FROM EntryData WHERE entryText = ?', (entryText,))
    db.commit()
    return redirect(url_for('fwiki.index'))