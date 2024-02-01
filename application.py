from flask import (
    Flask, render_template, request, redirect, send_from_directory, session, abort, url_for,
    jsonify
)
from datetime import date, datetime
from werkzeug.security import check_password_hash
from extensions import (db, mod_email, app_secretkey, BUCKET, links)
from utils import email_message, add_event_post, upload_file_to_s3
from flask_admin import Admin
from flask_login import LoginManager
from views import UserView


application = Flask(__name__, static_folder='static')
application.secret_key = app_secretkey


# renders the landing page with the event's data. It will exclude all events that precede the current date.
@application.route('/')
def landing():
    return render_template("home.html", current_year=date.today().year, events=db.events.find()[:3], today=date.today())


@application.route('/events')
def events():
    return render_template("index.html", current_year=date.today().year, events=db.events.find(), today=date.today())


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


@application.route('/sponsors')
def sponsors_page():
    return render_template('sponsors-page.html')


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


@application.get('/sponsors-tracking')
def sponsors_tracking():
    href = links[request.args["name"]]
    with open('sponsor-tracks.csv', 'a') as file:
        file.write(f'{datetime.now()},{request.args["name"]}\n')
    return redirect(href)


@application.get('/backup')
def backup_stored_data():
    response = upload_file_to_s3(
        file_path='sponsor-tracks.csv',
        bucket_name=BUCKET,
        key_name=f'sponsor-tracking/{datetime.now().strftime("%Y-%m")}.csv',
        region_name='us-west-1'
    )
    return jsonify({"response": response})


@application.route('/sitemap.xml')
def root_files():
    return send_from_directory(f"{application.static_folder}/root-files", 'sitemap.xml')


if __name__ == "__main__":
    # admin = Admin(application)
    # admin.add_view(UserView(db['admins']))
    application.run(debug=True)
