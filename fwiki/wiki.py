from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
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
    # TODO FIX THE WIKI NOT WORKING WHEN THERE IS NO ENTRYDATA
    row=get_db().execute('SELECT * FROM EntryData WHERE EntryData.title = ?', (title,)).fetchall().rowcount
    if row == 0:
        abort(404, "There is no entry data.")

    return render_template('wiki-pages/entry.html', entry=entry[0], info=entryInfo)


# TODO: This will be where our entries can be updated
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    entry = get_entry(id)

    if request.method == 'POST':
        title = request.form['title']
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
             # return redirect(url_for('blog.index'))

    return render_template('wiki/update.html', entry=entry)


#def get_entry(id, check_author=True):
#     entry = get_db().execute(
#         'SELECT *'
#         ' FROM Entry e JOIN User u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#    ).fetchone()
#
#     if post is None:
#         abort(404, "Entry id {0} doesn't exist.".format(id))
#
#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)
#
#     return post