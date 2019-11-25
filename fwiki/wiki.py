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
        'SELECT Entry.id, title, lastModified'
        ' FROM Entry JOIN EntryData ON Entry.id = EntryData.entryNumber'
        ' ORDER BY lastModified DESC'
    ).fetchall()
    return render_template('wiki-pages/index.html', posts=posts)