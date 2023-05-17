from flask import Flask, render_template, url_for, redirect, flash
from flask_migrate import Migrate
from flask_login import current_user

from database import models
from config import DeveloperConfig
from log.log import log
from authorization.authorization import authorization, login_manager


app = Flask(__name__)
app.config.from_object(DeveloperConfig())

app.register_blueprint(authorization, url_prefix='/authorization')

models.db.init_app(app)
login_manager.init_app(app)

migrate = Migrate(app, models.db)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', user=current_user)

if __name__ == "__main__":
    log.info('START SERVER')
    with app.app_context():
        models.db.create_all()
    app.run()
