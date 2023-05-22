from flask import Blueprint, render_template, request, redirect, url_for

from searchsustem.validater import ValidaterSearchText
from log.log import log
from database import models
from searchsustem.whoose import SearchText
from blog import constant, redis
from datetime  import timedelta

searchsustem = Blueprint('searchsustem', __name__, template_folder='templates')
    

@searchsustem.route('/<int:num>', methods=['GET'])
def search(num, text=None):
    """
    Обработчик поиска по сайту
    """
    # если text уже есть(нужно для работы запроса при пагинации)
    if text:
        search_text = text
    else:
        search_text = request.args['text']
        
    seacher = SearchText(search_text)

    # если не валидный запрос
    if not ValidaterSearchText(search_text)():
        return redirect(url_for('index'))
    
    # сначало берем все посты и ищим совпадения по тексту
    posts = models.Post.query.all()
    result = [post.text for post in posts if seacher(post.text)]
    log.warning(result)

    # теперь опять идем к БД но ищем только те посты которые соответствуют результату поиска и применяем пагинацию
    paginate = models.db.session.query(models.Post).filter(models.Post.text.in_(result)).order_by(models.Post.id.desc()).paginate(page=num, per_page=constant.PER_PAGE)
    per_page = paginate.has_prev
    next_page = paginate.has_next

    return render_template('searchsustem/search.html', text=search_text, posts=paginate, per_page=per_page, next_page=next_page, current_page=num, result=result)