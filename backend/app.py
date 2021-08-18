import os
import pymongo
from flask import Flask, render_template, request, session, send_from_directory
from flask_assets import Environment, Bundle
from flask.helpers import url_for
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import base64
from dotenv import load_dotenv

load_dotenv()

mongodbUser = os.getenv("MONGODB_USER")
mongodbPass = os.getenv("MONGODB_PASS")
sessionSecret = os.getenv("SESSION_SECRET")

app = Flask(__name__, static_url_path="", static_folder="../frontend")

assets = Environment(app)
# dirty trick to build all bundles, this gets angry when non-real files are
# passed to assets object


def updateBundles():
    for bundle in assets:
        bundle.urls()


app.jinja_env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")

client = pymongo.MongoClient(
    f"mongodb+srv://{mongodbUser}:{mongodbPass}@cluster0.xgwmg.mongodb.net/"
    + "Cluster0?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
)
app.secret_key = sessionSecret

# bundler for js and css
indexJS = Bundle("scripts/main.js", filters="jsmin", output="js/index.js")
indexCSS = Bundle("styles/main.css", filters="cssmin", output="css/index.css")
assets.register("js_index", indexJS)
assets.register("css_index", indexCSS)


# this method is called on every page load
def page_info(page):
    # sets url so that register/login/logout redirects correctly
    if "userApi" in page:
        session["url"] = "userApi"
        session["userpage"] = page.split("/")[1]
    else:
        session["url"] = page

        if "userpage" in session:
            session.pop("userpage", None)

    m = session["mod"] if "mod" in session else "0"
    session["mod"] = "0"

    e = session["err"] if "err" in session else None
    session["err"] = None

    # returns tuple with username, mod and err
    return (session["username"] if "username" in session else None, m, e)


# method gets and returns both binary images and linked sources
def get_image(img_dict, user=None):
    if "image" in img_dict:
        img = img_dict["image"].decode()
        imgStr = "data:image/png;base64,{0}".format(img)
    else:
        imgStr = img_dict["imageSrc"]

    return {
        "title": img_dict["title"],
        "caption": img_dict["caption"],
        "imageData": imgStr,
        "user": user or img_dict["user"],
    }


@app.route("/")
def index():
    db = client["users"]
    users = db["user1"]

    posts = users.find(projection={"username": True, "posts": True})
    images = []

    # get all existing posts and sort by time (most recent to oldest)
    for obj in posts:
        if "posts" in obj:
            for p in obj["posts"]:
                p["user"] = obj["username"]
                images.append(p)

    images.sort(
        key=lambda x: x["time"] if "time" in x else datetime(1970, 1, 1, 0, 0, 0, 0),
        reverse=True,
    )

    # up to 12 most recent posts will be displayed on the home page
    groups = []
    for i in range(min(len(images), 12)):
        groups.append(get_image(images[i]))

    p = page_info("index")

    return render_template(
        "index.pug",
        title="FOODSTAGRAM - HOME",
        username=p[0],
        mod_num=p[1],
        msg=p[2],
        images=groups,
        assetsName="index",
    )


profileJS = Bundle(
    "scripts/main.js", "scripts/profile.js", filters="jsmin", output="js/profile.js"
)
profileCSS = Bundle(
    "styles/main.css", "styles/profile.css", filters="cssmin", output="css/profile.css"
)
assets.register("js_profile", profileJS)
assets.register("css_profile", profileCSS)


@app.route("/user/<string:username>")
def userApi(username):
    db = client["users"]
    users = db["user1"]

    if not userExists(username):
        return "No such user exists"

    user = users.find_one({"username": username})
    updateBundles()

    # get posts from most recent to oldest
    posts = []
    for img in user["posts"]:
        posts.insert(0, get_image(img, username))

    p = page_info(f"userApi/{username}")

    following = False

    if p[0]:
        follow = users.find_one({"username": p[0]}, projection={"following": True})
        if "following" in follow and username in follow["following"]:
            following = True

    return render_template(
        "/profile.pug",
        title=f"FOODSTAGRAM - {username}",
        user=user,
        posts=posts,
        following=following,
        username=p[0],
        mod_num=p[1],
        msg=p[2],
        assetsName="profile",
    )


@app.route("/register", methods=["POST"])
def register():
    if "username" in session:
        return 405, "already logged in"

    db = client["users"]
    users = db["user1"]

    username = request.args.get("username") or request.form.get("username")
    password = request.args.get("password") or request.form.get("password")
    error = None

    if not username:
        error = "Username is required."
    elif " " in username:
        error = "Username can't have spaces"
    elif not password:
        error = "Password is required."
    # check if user exists already
    elif users.find_one({"username": username}) is not None:
        error = f"User {username} is already registered."

    # add user to db if no error from above
    if error is None:
        users.insert_one(
            {
                "username": username,
                "password": generate_password_hash(password),
                "followers": [],
                "following": [],
                "posts": [],
                "pfpSrc": "",
            }
        )
        session["mod"] = "2"
        # this is the reserve text -- shows that a user registered successfully
        # and can login below
        session["err"] = "Successfully registered; login below"
    else:
        session["mod"] = "1"
        session["err"] = error

    if "userpage" in session:
        u = session.pop("userpage", None)
        return redirect(url_for(session["url"], username=u))

    return redirect(url_for(session["url"]))


@app.route("/login", methods=["POST"])
def login():
    if "username" in session:
        return 405, "already logged in"

    db = client["users"]
    users = db["user1"]

    username = request.args.get("username") or request.form.get("username")
    password = request.args.get("password") or request.form.get("password")
    error = None
    user = users.find_one({"username": username}, projection={"password": True})

    if user is None:
        error = "Incorrect username."
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password."

    if error is not None:
        session["err"] = error
        session["mod"] = "2"
    else:
        session["username"] = username

    if "userpage" in session:
        u = session.pop("userpage", None)
        return redirect(url_for(session["url"], username=u))

    return redirect(url_for(session["url"]))


@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username", None)

    if "userpage" in session:
        u = session.pop("userpage", None)
        return redirect(url_for(session["url"], username=u))

    return redirect(url_for(session["url"]))


def userExists(username):
    db = client["users"]
    users = db["user1"]
    if users.find_one({"username": username}) is None:
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


@app.route("/createPost", methods=["POST"])
def createPost():
    if "username" not in session:
        return 401, "Must be logged in"

    username = session["username"]

    db = client["users"]
    users = db["user1"]

    title = request.args.get("title") or request.form.get("title")
    caption = request.args.get("caption") or request.form.get("caption")
    file = request.files["imageSrc"]
    imageSrc = request.args.get("imageSrc") or file.filename
    redirectURL = request.args.get("returnURL") or request.form.get("returnURL")
    time = datetime.now()

    image = base64.b64encode(file.read())

    users.find_one_and_update(
        {"username": username},
        {
            "$push": {
                "posts": {
                    "title": title,
                    "caption": caption,
                    "imageSrc": imageSrc,
                    "image": image,
                    "time": time,
                }
            }
        },
        upsert=True,
    )
    return redirect(redirectURL)


# update post takes four parameters
# index, the position of the element in the posts array
# title, the new title of the post
# caption, the new caption of the post
# imageSrc, the new image url of the post
@app.route("/updatePost", methods=["POST"])
def updatePost():
    if "username" not in session:
        return 401, "Must be logged in"

    username = session["username"]

    db = client["users"]
    users = db["user1"]

    index = request.args.get("index") or request.form.get("index")
    title = request.args.get("title") or request.form.get("title")
    caption = request.args.get("caption") or request.form.get("caption")
    imageSrc = request.args.get("imageSrc") or request.form.get("imageSrc")
    # to be implemented, probably preferable to increment likes and append comments to the comments array
    # also probably preferable not to set every single property of the object, rather to only set the properties that are being changed
    # likes = request.args.get("likes") or request.form.get("likes")
    # comments = request.args.get("comment") or request.form.get("comment")

    users.find_one_and_update(
        {"username": username},
        {
            "$set": {
                f"posts.{index}.title": title,
                f"posts.{index}.caption": caption,
                f"posts.{index}.imageSrc": imageSrc,
            }
        },
    )
    return "200"


# deletes a post takes one parameter
# index, the position of the element in the posts array


@app.route("/deletePost", methods=["POST"])
def deletePost():
    if "username" not in session:
        return 401, "Must be logged in"

    username = session["username"]

    db = client["users"]
    users = db["user1"]

    index = request.args.get("index") or request.form.get("index")

    users.find_one_and_update({"username": username}, {"$unset": {f"posts.{index}": 1}})
    users.find_one_and_update({"username": username}, {"$pull": {"posts": None}})
    return "200"


# lets assume there are no privacy options for the moment
# get post takes two parameters
# username, the owner of the post
# index, the index of the post in the owner's post array
# returns a post


@app.route("/getPost", methods=["POST"])
def getPost():
    db = client["users"]
    users = db["user1"]

    username = request.args.get("username") or request.form.get("username")
    if not userExists(username):
        return "No such user exists"
    index = int(request.args.get("index") or request.form.get("index"))

    posts = users.find_one({"username": username}, projection={"posts": True})["posts"]
    if posts is None:
        return "This user has no posts"
    if index >= len(posts) or index < 0:
        return "No such post exists"
    requestedPost = posts[index]
    if requestedPost is None:
        return "No such post exists"
    else:
        return requestedPost


@app.route("/follow/<string:username>", methods=["POST"])
def follow(username):
    db = client["users"]
    users = db["user1"]

    currUser = session["username"] if "username" in session else None
    if currUser is None:
        return "401"

    users.find_one_and_update(
        {"username": username},
        {
            "$push": {
                "followers": currUser,
            }
        },
        upsert=True,
    )

    users.find_one_and_update(
        {"username": currUser},
        {
            "$push": {
                "following": username,
            }
        },
        upsert=True,
    )

    if "userpage" in session:
        u = session.pop("userpage", None)
        return redirect(url_for(session["url"], username=u))

    return redirect(url_for(session["url"]))


@app.route("/unfollow/<string:username>", methods=["POST"])
def unfollow(username):
    db = client["users"]
    users = db["user1"]

    currUser = session["username"] if "username" in session else None
    if currUser is None:
        return "401"

    users.find_one_and_update(
        {"username": username},
        {
            "$pull": {
                "followers": currUser,
            }
        },
        upsert=True,
    )

    users.find_one_and_update(
        {"username": currUser},
        {
            "$pull": {
                "following": username,
            }
        },
        upsert=True,
    )

    if "userpage" in session:
        u = session.pop("userpage", None)
        return redirect(url_for(session["url"], username=u))

    return redirect(url_for(session["url"]))


# server side functions for getting posts,
def serverGetPost(username, index):
    db = client["users"]
    users = db["user1"]

    if not userExists(username):
        return "No such user exists"

    posts = users.find_one({"username": username}, projection={"posts": True})["posts"]
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
    db = client["users"]
    users = db["user1"]

    if not userExists(username):
        return []

    posts = users.find_one({"username": username}, projection={"posts": True})

    return posts["posts"] if "posts" in posts else []


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


updateBundles()
