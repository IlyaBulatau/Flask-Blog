from flask import Blueprint, render_template, request, redirect, url_for

from searchsustem.validater import ValidaterSearchText
from log.log import log
from database import models
from searchsustem.whoose import full_text_search

searchsustem = Blueprint('searchsustem', __name__, template_folder='templates')
    

@searchsustem.route('/', methods=['GET'])
def search():
    search_text = request.args['text']

    if not ValidaterSearchText(search_text)():
        return redirect(url_for('index'))

    log.warning(search_text)
    posts = models.Post.query.all()
    result = [post for post in posts if full_text_search(search_text, post.text)]

    return render_template('searchsustem/search.html', text=search_text, posts=result)