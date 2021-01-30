"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = '/static/panda.png'


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    '''Creating User table'''

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False, default=DEFAULT_IMAGE_URL)
    posts = db.relationship('Post', backref='user')

    @property
    def full_name(self):
        """Return full name of a User"""

        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    '''Creating Post table'''

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return formatted date."""

        return self.created_at.strftime("%a, %b %-d,  %Y, %-I:%M %p")


class PostTag(db.Model):
    '''Creating link model between Post and Tag tables'''

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),
                        primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'),
                       primary_key=True, nullable=False)


class Tag(db.Model):
    '''Creating Tag table'''

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False, unique=True)

    posts = db.relationship('Post',
                            secondary='posts_tags',
                            backref='tags')
