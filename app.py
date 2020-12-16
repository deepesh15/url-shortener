from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class URLS(db.Model):
    id_ = db.Column('id_',db.Integer,primary_key = True)
    longURL = db.Column('longURL',db.String())
    shortURL = db.Column('shortURL',db.String(6))

    def __init__(self, longURL,shortURL):
        self.longURL = longURL
        self.shortURL = shortURL

#create table
def create_tables():
    db.create_all()

def shorten_url():
    letters = string.ascii_lowercase +string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters,k=6)
        rand_letters = "".join(rand_letters)
        #check if the shorten URL code already exists
        short_url = URLS.query.filter_by(shortURL= rand_letters).first()
        if not short_url:
            return rand_letters

@app.route('/', methods =['POST','GET'])
def index():
    if request.method == "POST":    #if method is POST use the url_input and shorten it.
        url_input = request.form["url_input"]
        #check if the URL already exists in the DB
        found_url = URLS.query.filter_by(longURL=url_input).first()
        if found_url:
            #returh short url if found.
            return redirect(url_for("display_short_url",url=found_url.shortURL))
        else:
            #create a short URL if it is not in DB
            short_url = shorten_url()
            new_url = URLS(url_input,short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url",url=short_url))
    else:                           #if method is not POST just display the landing page
        return render_template("index.html")

@app.route('/display/<url>')
def display_short_url(url):
    return render_template("short.html",short_url_display=url)

@app.route('/<short_url>')
def redirection(short_url):
    long_url = URLS.query.filter_by(shortURL =  short_url).first()
    if long_url:
        return redirect(long_url.longURL)
    else:
        return f'<h1>URL does not exist'

if __name__ == "__main__":
    app.run(port=5000,debug=True)
    