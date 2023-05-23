from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user
from flask_login import login_required

from datetime import timedelta

from blog.forms import PostAddForm, PostChangeForm, CommentAddForm, CommentChangeForm
from database import models
from blog import constant
from log.log import log
from blog.service import replace_tag_in_text
from blog.redis import redis

blog = Blueprint('blog', __name__, template_folder='templates')

@blog.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    """
    Обработчик страницы добавлени постов
    """
    form = PostAddForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            text = form.text.data
            user_id = current_user.id

            post = models.Post(
                title=title,
                text=text,
                user_id=user_id
            )
            # запись в хэш юзер ид для ограничения публикации постов
            redis.set(current_user.id, current_user.id, ex=timedelta(days=constant.LIMIT_POST))
            models.db.session.add(post)
            models.db.session.commit()
            log.info(f'User in id: {post.user_id} add new post - title {post.title}')
            return redirect(url_for('index'))
    return render_template('blog/add_post.html', form=form)

@blog.route('/view_posts/page=<int:num>')
def view_posts(num):
    """
    Обработчик страницы отображения всех постов
    """
    posts = models.Post.query.order_by(models.Post.id.desc()).paginate(page=num, per_page=constant.PER_PAGE)
    prev_page = posts.has_prev
    next_page = posts.has_next

    return render_template('blog/view_posts.html', posts=posts, prev_page=prev_page, next_page=next_page, current_page=num)

@blog.route('/<string:title>', methods=['GET', 'POST'])
def show_post(title):
    """
    Обработчик страницы просмотра конкретного поста и добавления комментариев
    """
    form = CommentAddForm()
    post = models.Post.query.filter(models.Post.title == title).first()
    if request.method == 'POST':
        # добавления омментария к посут    
        if form.validate_on_submit():
            text_comment = form.text.data

            comment = models.Comment(
                text=text_comment,
                user_id=current_user.id,
                post_id=post.id
            )
            models.db.session.add(comment)
            models.db.session.commit()

            return redirect(url_for('.show_post', title=post.title))
        
    return render_template('blog/show_post.html', post=post, form=form)

@blog.route('/mypost')
@login_required
def my_post():
    """
    Обработчик просмотра постов юзера по его ид
    """
    posts = models.Post.query.order_by(models.Post.id.desc()).filter(models.Post.user_id == current_user.id).all()
    return render_template('blog/mypost.html', posts=posts)

@blog.route('/<string:title>/change', methods=['GET', 'POST'])
@login_required
def change_post(title):
    """
    Обработчик изменения поста юзером
    """
    post = models.Post.query.filter(models.Post.title == title).first()
    form = PostChangeForm(text=post.text)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_text = replace_tag_in_text(form.text.data)

        # если пользователь нажал кнопку save
        if form.save.data:
            # если он внес какие либо изменения в текст поста
            if new_text != post.text:
                post.text = new_text
                models.db.session.commit()

        return redirect(url_for('.my_post'))
    return render_template('blog/change_post.html', form=form, title=title)

@blog.route('commentchange/<string:title>/<string:comment_id>', methods=['GET', 'POST'])
def change_comment(title, comment_id):
    """
    Обработчик изменения комментария
    """
    comment = models.Comment.query.filter(models.Comment.id == comment_id).first()
    form = CommentChangeForm(text=comment.text)
    if request.method == 'POST':
        if form.validate_on_submit():
            text = replace_tag_in_text(form.text.data)

            if form.save.data:
                if text != comment.text:
                    comment.text = text
                    models.db.session.commit()
            return redirect(url_for('.show_post', title=title))
    return render_template('blog/change_comment.html', form=form)


@blog.route('<string:title>/delete')
@login_required
def del_post(title):
    post = models.Post.query.filter(models.Post.title == title).first()
    models.db.session.delete(post)
    models.db.session.commit()
    return redirect(url_for('.my_post'))

@blog.route('/deletecomment<string:comment_id>/<string:title>')
def delete_comment(comment_id, title):
    comment = models.Comment.query.filter(models.Comment.id == comment_id).first()
    if comment.user.id == current_user.id:
        models.db.session.delete(comment)
        models.db.session.commit()
    return redirect(url_for('.show_post', title=title))