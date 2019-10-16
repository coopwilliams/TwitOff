# Flask makes app objects
from flask import Flask, render_template

# create Flask web server
app = Flask(__name__)

# routes determine location
@app.route("/")

# define a simple function
def home():
    return render_template("home.html")

@app.route("/about")
def preds():
    return render_template("about.html")

@app.route("/dummy")
def abuse():
    return render_template("dummy.html")
