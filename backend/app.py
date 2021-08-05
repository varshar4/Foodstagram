import os
import pymongo
import pprint
from flask import Flask, render_template, send_from_directory, request
from dotenv import load_dotenv

load_dotenv()

mongodbUser = os.getenv("MONGODB_USER")
mongodbPass = os.getenv("MONGODB_PASS")

app = Flask(__name__, static_url_path='', static_folder='../frontend/project')
client = pymongo.MongoClient(f"mongodb+srv://{mongodbUser}:{mongodbPass}@cluster0.xgwmg.mongodb.net/Cluster0?retryWrites=true&w=majority")

@app.route('/')
def index():
    return "This works!", 200

@app.route('/dbtest')
def dbtest():
  db = client['sample_airbnb']
  users = db['listingsAndReviews']
  data = list(users.find({})[:50])

  return render_template('dbtest.html', title="Database Test", data=data, url=os.getenv("URL"))


