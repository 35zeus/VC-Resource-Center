from flask import Flask, render_template, request, redirect, send_from_directory, session, abort
from datetime import date
from werkzeug.security import check_password_hash
from extensions import (db, mod_email, app_secretkey)
from functools import wraps
from utils import email_message


application = Flask(__name__, static_folder='static')
application.secret_key = app_secretkey


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if session["admin"]:
            return func(*args, **kwargs)
        else:
            return abort(403)
    return decorated_view


# renders the landing page with the event's data. It will exclude all events that precede the current date.
@application.route('/')
def landing():
    return render_template("home.html", current_year=date.today().year, events=db.events.find()[:3], today=date.today())


@application.route('/events')
def events():
    return render_template("index.html", current_year=date.today().year,  events=db.events.find(), today=date.today())


@application.route('/add-event', methods=["GET", "POST"])
@admin_required
def add_event():
    return "Hello"


# gets the post selected data and displays it as a full page
@application.route('/post')
def get_full_post():
    id_num = int(request.args["id_num"])
    post_data = None

    for event in db.events.find():
        if event["post_id"] == id_num:
            post_data = event

    return render_template('full-post.html', post_data=post_data, current_year=date.today().year)


@application.route('/donate')
def get_donation_page():
    return render_template('donations.html', current_year=date.today().year)


# a route for the footer on any html page to go to in order to send a notification that someone has signed up for the
# newsletter.
@application.route('/sign-up', methods=['POST'])
def newsletter_signup():
    name = request.form['name']
    email = request.form['email']
    if check_password_hash(db.admins.find_one({"user_id": 1})["hash"], email):
        session["admin"] = True
    else:
        email_message(name, email)
        email_message(name, email, to_email=mod_email)
    return redirect('/')


@application.route('/about-us')
def about_us():
    return render_template("about.html", current_year=date.today().year)


@application.route('/contact-us')
def get_contact_page():
    return render_template("contact.html", current_year=date.today().year)


# Adds string stating the contact form sending was successful (since I don't know JS yet)
@application.route('/contact-success')
def get_contact_success_page():
    return render_template('contact-success.html', current_year=date.today().year)


# Takes in contact form data from contact.html to send to administrator's email
@application.route('/submit', methods=['POST'])
def get_form_sent():
    if request.method == 'POST':
        contact_name = request.form['contact-name']
        contact_email = request.form['contact-email']
        category = request.form['category']
        message = request.form['message']
        email_message(contact_name, contact_email, message, category)
        email_message(contact_name, contact_email, message, category, to_email=mod_email)
    return application.redirect('/contact-success')


@application.route('/sitemap.xml')
def root_files():
    return send_from_directory(f"{application.static_folder}/root-files", 'sitemap.xml')


if __name__ == "__main__":
    application.run(debug=True)
