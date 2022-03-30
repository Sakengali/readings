from flask import Flask, render_template, request
import csv
from flask_mail import Mail, Message
import os

app = Flask(__name__)

app.config["MAIL_DEFAULT_SENDER"] = None
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config["MAIL_PORT"] = 465
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True   
mail = Mail(app)

WRITERS = [
    "Khaled Hosseini",
    "Jane Austen",
    "Edgar Allan Poe",
    "Agatha Cristie",
    "Arthur Conan Doyle"
]

SUBSCRIBERS = {}

@app.route("/")
def index():
    return render_template("index.html", writers=WRITERS)

@app.route("/subscription", methods=["POST"])
def subscribe():

    name = request.form.get("sub_name")
    if not name:
        return render_template("error.html", error_message="Missing name")
    
    email = request.form.get("email")
    if not email:
        return render_template("error.html", error_message="Missing email")
    
    writer_name = request.form.get("writer_name")
    if not writer_name :
        return render_template("error.html", error_message="Missing writer's name")
    
    if writer_name not in WRITERS:
        return render_template("error.html", error_message="Invalid writer")

    sub_info = f"{name}, {email}"

    SUBSCRIBERS[sub_info] = writer_name 
 
    with open("sub_database.csv", "a") as file:
        writer=csv.writer(file)
        writer.writerow((sub_info, writer_name))

    message=Message(f"{name}, you are registered for the books of {writer_name}.", sender="kazhievb@gmail.com", recipients=[email])
    mail.send(message)  

    return render_template("subscription.html", writer = writer_name, name = name)


@app.route("/subscribers")
def subscribers():
    return render_template("subscribers.html", subscribers=SUBSCRIBERS)
