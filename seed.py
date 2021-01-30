from models import User, Post, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name='Van', last_name='Helsing',
          image_url='https://pngimg.com/uploads/cat/cat_PNG50505.png')
u2 = User(first_name='Andy', last_name='Nielsen',
          image_url='https://www.pinclipart.com/picdir/big/173-1733627_clipart-ear-micky-mouse-mickey-mouse-face-transparent.png')
u3 = User(first_name='Pauline', last_name='Quinn')

p1 = Post(title='Garlic bread',
          content='Pls need a recipe, asking for a friend', user_id='1')
p2 = Post(title='Read me !',
          content='Starting a vacation blog soon, stay tuned for the first post about Greece', user_id='2')
p3 = Post(title='Toothpaste explosion',
          content='Hi all, giving tips for the elephant toothpaste explosion on this channel', user_id='3')

t1 = Tag(name='fun')
t2 = Tag(name='weird')
t3 = Tag(name='smart')

db.session.add_all([u1, u2, u3])

db.session.commit()

db.session.add_all([p1, p2, p3])

db.session.commit()

t1 = Tag(name='fun')
t2 = Tag(name='weird')
t3 = Tag(name='smart')

db.session.add_all([t1, t2, t3])

db.session.commit()
