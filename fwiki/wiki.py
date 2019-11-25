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

# def get_entry(id, check_author=True):
#     entry = get_db().execute(
#         'SELECT *'
#         ' FROM Entry e JOIN User u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()
#
#     if post is None:
#         abort(404, "Entry id {0} doesn't exist.".format(id))
#
#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)
#
#     return post