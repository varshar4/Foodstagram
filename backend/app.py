import os
import pymongo
from flask import Flask, render_template, send_from_directory, request, session
from flask_assets import Environment, Bundle
import cssmin
from jsmin import jsmin
from flask.helpers import url_for
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

load_dotenv()

mongodbUser = os.getenv("MONGODB_USER")
mongodbPass = os.getenv("MONGODB_PASS")
sessionSecret = os.getenv("SESSION_SECRET")

app = Flask(__name__, static_url_path='', static_folder='../frontend/project')

assets = Environment(app)

app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

client = pymongo.MongoClient(
    f"mongodb+srv://{mongodbUser}:{mongodbPass}@cluster0.xgwmg.mongodb.net/Cluster0?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
)
app.secret_key = sessionSecret

# bundler for js and css
indexJS = Bundle('scripts/main.js', filters='jsmin', output='js/index.js')
indexCSS = Bundle('styles/main.css',
                  filters='cssmin', output='css/index.css')
assets.register('js_index', indexJS)
assets.register('css_index', indexCSS)



def user():
    return session['username'] if 'username' in session else None


@app.route('/')
def index():
    m = session['mod'] if 'mod' in session else '0'
    session['mod'] = '0'
    e = session['err'] if 'err' in session else None
    session['err'] = None
    session['url'] = 'index'
    return render_template('index.pug', title='FOODSTAGRAM - HOME', username=user(), mod_num=m, msg=e, assetsName='index')


profileJS = Bundle('scripts/main.js', filters='jsmin', output='js/profile.js')
profileCSS = Bundle('styles/main.css', 'styles/profile.css',
                    filters='cssmin', output='css/profile.css')
assets.register('js_profile', profileJS)
assets.register('css_profile', profileCSS)


@app.route('/profileTest')
def profileTest():
    m = session['mod'] 
    session['mod'] = '0'
    e = session['err']
    session['err'] = None
    session['url'] = 'profileTest'
    return render_template('profile.pug', title='FOODSTAGRAM - PROFILE', username=user(), mod_num=m, msg=e, assetsName='profile')


@app.route('/main')
def main():
    username = session['username'] or None
    if username is None:
        return redirect(url_for('login'))
    return render_template('main.html', title="Main content", username=username, url=os.getenv("URL"))


@app.route('/register', methods=['POST'])
def register():
    db = client['users']
    users = db['user1']

    username = request.args.get('username') or request.form.get('username')
    password = request.args.get('password') or request.form.get('password')
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    # check if user exists already
    elif users.find_one({'username': username}) is not None:
        error = f"User {username} is already registered."
    
    # add user to db if no error from above
    if error is None:
        users.insert_one({'username': username, 'password': generate_password_hash(password)})
        session['mod'] = '2'
        session['err'] = "Successfully registered; login below" # this is the reserve text 
    else:
        session['mod'] = '1'
        session['err'] = error
    
    return redirect(url_for(session['url']))

# reserve text is the text that the register page may send to show that a user registered successfully and can login below


@app.route('/login', methods=['POST'])
def login():
    db = client['users']
    users = db['user1']

    username = request.args.get('username') or request.form.get('username')
    password = request.args.get('password') or request.form.get('password')
    error = None
    user = users.find_one({'username': username}, projection={"password": True})

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is not None:
        session['err'] = error
        session['mod'] = '2'
    else:
        session['username'] = username
    
    return redirect(url_for(session['url']))


@app.route('/logout')
def logout():
    if 'username' in session: 
        session.pop('username', None)

    return redirect(url_for(session['url']))


def userExists(username):
    db = client['users']
    users = db['user1']
    if users.find_one({'username': username}) is None:
        print("user does not exist")
        return False
    else:
        print("user exists")
        return True

# index is the iterator of the chronological order of posts

# creates the post takes three parameters
# title, the title of the post
# caption, the caption of the post
# imageSrc, the image url of the post


@app.route('/createPost', methods=['POST'])
def createPost():
    username = session['username'] or None
    if username is None:
        return "401"

    db = client['users']
    users = db['user1']

    title = request.args.get('title') or request.form.get('title')
    caption = request.args.get('caption') or request.form.get('caption')
    imageSrc = request.args.get('imageSrc') or request.form.get('imageSrc')

    users.find_one_and_update({"username": username}, {"$push": {'posts': {
                              'title': title, 'caption': caption, 'imageSrc': imageSrc}}}, upsert=True)
    return "200"


# update post takes four parameters
# index, the position of the element in the posts array
# title, the new title of the post
# caption, the new caption of the post
# imageSrc, the new image url of the post
@app.route('/updatePost', methods=['POST'])
def updatePost():
    username = session['username'] or None
    if username is None:
        return "401"

    db = client['users']
    users = db['user1']

    index = request.args.get('index') or request.form.get('index')
    title = request.args.get('title') or request.form.get('title')
    caption = request.args.get('caption') or request.form.get('caption')
    imageSrc = request.args.get('imageSrc') or request.form.get('imageSrc')

    users.find_one_and_update({"username": username}, {'$set': {
                              f'posts.{index}.title': title, f'posts.{index}.caption': caption, f'posts.{index}.imageSrc': imageSrc}})
    return "200"

# deletes a post takes one parameter
# index, the position of the element in the posts array


@app.route('/deletePost', methods=['POST'])
def deletePost():
    username = session['username'] or None
    if username is None:
        return "401"

    db = client['users']
    users = db['user1']

    index = request.args.get('index') or request.form.get('index')

    users.find_one_and_update({"username": username}, {
                              "$unset": {f"posts.{index}": 1}})
    users.find_one_and_update({"username": username}, {
                              '$pull': {"posts": None}})
    return "200"

# lets assume there are no privacy options for the moment
# get post takes two parameters
# username, the owner of the post
# index, the index of the post in the owner's post array
# returns a post


@app.route('/getPost', methods=['POST'])
def getPost():
    db = client['users']
    users = db['user1']

    username = request.args.get('username') or request.form.get('username')
    if userExists(username) == False:
        return "No such user exists"
    index = int(request.args.get('index') or request.form.get('index'))

    posts = users.find_one({"username": username}, projection={
                           "posts": True})['posts']
    if posts is None:
        return "This user has no posts"
    if index >= len(posts) or index < 0:
        return "No such post exists"
    requestedPost = posts[index]
    if requestedPost is None:
        return "No such post exists"
    else:
        return requestedPost

# server side functions for getting posts,


def serverGetPost(username, index):
    db = client['users']
    users = db['user1']

    if userExists(username) == False:
        return "No such user exists"

    posts = users.find_one({"username": username}, projection={
                           "posts": True})['posts']
    if posts is None:
        return "This user has no posts"
    if index >= len(posts) or index < 0:
        return "No such post exists"
    requestedPost = posts[index]
    if requestedPost is None:
        return "No such post exists"
    else:
        return requestedPost


def serverGetAllPosts(username):
    db = client['users']
    users = db['user1']

    if userExists(username) == False:
        return []

    posts = users.find_one({"username": username}, projection={"posts": True})
    
    return posts['posts'] if 'posts' in posts else []


@app.route('/dbtest')
def dbtest():
    user = request.args.get("username")
    posts = []
    if user is not None:
        posts = serverGetAllPosts(user)

    return render_template('dbtest.html', title="Database Test", data=posts, url=os.getenv("URL"))


# dirty trick to build all bundles, this gets angry when non-real files are passed to assets object
for bundle in assets:
    bundle.urls()
