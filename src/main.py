from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import current_user
from flask_ckeditor import CKEditor
from flask_debugtoolbar import DebugToolbarExtension

from database import models
from config import DeveloperConfig
from log.log import log
from authorization.authorization import authorization, login_manager
from blog.blog import blog
from blog.redis import redis
from searchsustem.searchsustem import searchsustem
from errors import errors, handlers


app = Flask(__name__)
app.config.from_object(DeveloperConfig())

app.register_blueprint(authorization, url_prefix='/authorization')
app.register_blueprint(blog, url_prefix='/blog')
app.register_blueprint(searchsustem, url_prefix='/search')
app.register_blueprint(errors.errors)
app.logger.addHandler(log)
app.redis = redis

app.register_error_handler(404, handlers.not_found)
app.register_error_handler(500, handlers.server_error)

models.db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'authorization.login'

migrate = Migrate(app, models.db)

ckeditor = CKEditor(app)

toolbar = DebugToolbarExtension(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', user=current_user)

if __name__ == "__main__":
    log.info('START SERVER')
    with app.app_context():
        models.db.create_all()
    app.run()

#TODO - 
# Обработка ошибок
# Добавить возможность перевода текста