from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin



db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger(), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(16), nullable=False)
    create_time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')
    
    def __repr__(self):
        return f'User: {self.username}, E-mail: {self.email}'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.BigInteger(), primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    text = db.Column(db.Text(), nullable=False)
    create_time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    user_id = db.Column(db.BigInteger(), db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post')

    def __repr__(self):
        return f'{self.title} from user id {self.user_id}'
    

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.BigInteger(), primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    create_time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    user_id = db.Column(db.BigInteger(), db.ForeignKey('users.id'))
    post_id = db.Column(db.BigInteger(), db.ForeignKey('posts.id'))

    def __repr__(self):
        return f'Id Coment {self.id} from user id {self.user_id}, post id {self.post_id}'