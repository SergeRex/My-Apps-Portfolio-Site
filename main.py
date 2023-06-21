import os

import yagmail
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

#import pymysql


app = Flask(__name__)
app.app_context().push()

URL_GCLOUD_MYSQL_DB = os.environ.get('MY_URL_GCLOUD_MYSQL_DB')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{URL_GCLOUD_MYSQL_DB}"

db = SQLAlchemy(app)


class Myapps(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.VARCHAR(255), nullable=False)
    show_order = db.Column(db.INTEGER, nullable=False)
    brief = db.Column(db.VARCHAR(1000), nullable=False)
    tools = db.Column(db.VARCHAR(250), nullable=False)
    img1 = db.Column(db.VARCHAR(250), nullable=False)
    img2 = db.Column(db.VARCHAR(250), nullable=False)
    img3 = db.Column(db.VARCHAR(250), nullable=False)
    img_header = db.Column(db.VARCHAR(250), nullable=False)
    app_link = db.Column(db.VARCHAR(250), nullable=False)
    source_code = db.Column(db.VARCHAR(250), nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    description2 = db.Column(db.VARCHAR(2000), nullable=False)
    video_link = db.Column(db.VARCHAR(250), nullable=True)


my_portfolio = Myapps.query.all()
my_portfolio = sorted(my_portfolio, key=lambda k: k.show_order, reverse=False)


@app.route("/")
def get_all_my_apps():
    return render_template("index.html",all_apps=my_portfolio)


@app.route("/myapp/<int:index>")
def show_my_app(index):
    requested_app = None
    for my_app in my_portfolio:
        if my_app.id == index:
            requested_app = my_app
    return render_template("my_app.html", my_app=requested_app)


@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data)
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email (name, email, phone, message):

    MY_EMAIL = os.environ.get('MY_EMAIL_ADDRESS')
    MY_PASSWORD = os.environ.get('MY_EMAIL_PASSWORD')

    email_subject = "Message from my portfolio site"
    email_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
    with yagmail.SMTP(MY_EMAIL, MY_PASSWORD) as msg:
        msg.send(MY_EMAIL, email_subject, email_message)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)