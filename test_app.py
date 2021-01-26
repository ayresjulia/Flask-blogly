from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-blogly-test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name="Angelina", last_name="Jolie",
                    image_url='https://toppng.com/public/uploads/thumbnail/orange-lotus-transparent-11563886428cy0ducwwby.png')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_all_users_page(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Angelina', html)

    def test_user_edit(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Angelina Jolie', html)

    def test_create_user(self):
        with app.test_client() as client:
            test = {"first_name": "Brad", "last_name": "Pitt",
                    "image_url": 'https://toppng.com/public/uploads/thumbnail/orange-lotus-transparent-11563886428cy0ducwwby.png'}
            resp = client.post("/users/new", data=test, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                "<h3>Click on a User to get more details:</h3>", html)
