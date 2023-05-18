from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user
from flask_login import login_required

from blog.forms import PostAddForm, PostChangeForm
from database import models
from blog import constant
from log.log import log
from blog.service import replace_tag_in_text

blog = Blueprint('blog', __name__, template_folder='templates')

@blog.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
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

            models.db.session.add(post)
            models.db.session.commit()
            return redirect(url_for('index'))
    return render_template('blog/add_post.html', form=form)

@blog.route('/view_posts/page=<int:num>')
def view_posts(num):
    posts = models.Post.query.order_by(models.Post.id.desc()).paginate(page=num, per_page=constant.PER_PAGE)
    prev_page = posts.has_prev
    next_page = posts.has_next

    return render_template('blog/view_posts.html', posts=posts, prev_page=prev_page, next_page=next_page, current_page=num)

@blog.route('/<string:title>')
def show_post(title):
    post = models.Post.query.filter(models.Post.title == title).first()
    return render_template('blog/show_post.html', post=post)

@blog.route('/mypost')
def my_post():
    posts = models.Post.query.order_by(models.Post.id.desc()).filter(models.Post.user_id == current_user.id)
    return render_template('blog/mypost.html', posts=posts)

@blog.route('/<string:title>/change', methods=['GET', 'POST'])
def change_post(title):
    post = models.Post.query.filter(models.Post.title == title).first()
    form = PostChangeForm(text=post.text)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_text = replace_tag_in_text(form.text.data)

        if form.save.data:
            if new_text != post.text:
                post.text = new_text
                models.db.session.commit()

        return redirect(url_for('.my_post'))
    return render_template('blog/change_post.html', form=form, title=title)