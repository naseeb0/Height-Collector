from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
import email

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='postgres://postgres:nashib@localhost/height'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://pcycopbizjjths:d530c1db63aab18caeab4ddfcd5584f4cfc5bbda6d8434ece84bc3edfbf0518a@ec2-34-200-72-77.compute-1.amazonaws.com:5432/dfdmaq5a1d5t2k?sslmode=require'
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_=email_
        self.height_=height_

@app.route("/")
def index():
    return render_template("index.html")
 

@app.route("/success", methods=["POST"])
def success():
    if request.method=="POST":
        email = request.form["email_name"]
        height = request.form['height_name']
        send_email(email, height)
        if db.session.query(Data).filter(Data.email_ ==email).count() ==0:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            return render_template("success.html")
    return render_template('index.html',
    text = "Looks Like We have already got some request from that email. :-) ")

if __name__ =="__main__":
    app.debug = True
    app.run()
