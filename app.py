from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cocopuff007'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    '''Redirects to users list page'''

    return redirect('/users')


@app.route('/users')
def all_users_page():
    '''Shows list of all users in db'''

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def create_new_form():
    '''View blank user form to create a new user'''

    return render_template('form.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    '''Create a new user and add to the user list'''

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_edit(user_id):
    '''Show edit page for a user'''

    user = User.query.get_or_404(user_id)

    return render_template('details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit_form(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('editform.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    '''Edit info about the user'''

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

##### Post routes #####


@app.route('/users/<int:user_id>/posts/new')
def post_form(user_id):
    """Show a form to add a post for an existing user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('postform.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    '''Add a new post'''

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''Show users post'''

    post = Post.query.get_or_404(post_id)

    return render_template('showpost.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def update_post(post_id):
    '''Show form to edit user's post'''

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('editpost.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    '''Edit user's post'''

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''Delete user's post'''

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')


##### Tag routes #####
@app.route('/tags')
def get_tag():
    '''List of all Tags'''

    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    '''Show tag detail, allow to edit'''

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tagdetails.html', tag=tag)


@app.route('/tags/new')
def tag_form():
    '''Show a form to add a new tag'''

    posts = Post.query.all()
    return render_template('newtag.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/edit')
def tag_edit_form(tag_id):
    '''Show a form to edit a new tag'''

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edittag.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Update existing Tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tags(tag_id):
    """Delete existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
