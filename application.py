from flask import Flask, render_template, request, redirect
from datetime import date, datetime
from smtplib import SMTP
import os
import requests
from dotenv import load_dotenv

application = Flask(__name__)
application.secret_key = os.urandom(12).hex()

year = date.today().year
today = date.today()

load_dotenv()


# The following function takes env variables of the moderators email credentials, formats an email to the correct
# recipient and sends the email.
def email_message(
        name, contact_email,
        body='New Sign up for the newsletter',
        category='Newsletter',
        recipient_email=os.environ.get('RECIPIENT_EMAIL')
):
    sending_email = os.environ.get('MOD_EMAIL')
    sending_password = os.environ.get('MOD_EMAIL_PASSWORD')
    with SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=sending_email, password=sending_password)
        connection.sendmail(
            from_addr=sending_email,
            to_addrs=recipient_email,
            msg=f'Subject:Contact Form Submission\n\nFrom: {name} at {contact_email}\n'
                f'Category: {category}\n'
                f'Message: {body}',
        )


# renders the landing page with the events data. It will exclude all events that precede the current date.
@application.route('/')
def landing():
    events_json = requests.get('https://api.npoint.io/a0fbacdbf8f5e6a731a3').json()
    for x in range(len(events_json)):
        my_date = events_json[x]["date"]
        date_object = datetime.strptime(my_date, '%Y-%m-%d').date()
        events_json[x]["date"] = date_object
    return render_template("index.html", current_year=year, events=events_json, today=today)


@application.route('/about-us')
def about_us():
    return render_template("about.html", current_year=year)


@application.route('/contact-us')
def get_contact_page():
    return render_template("contact.html", current_year=year)


# Adds string stating the contact form sending was successful (since I don't know JS yet)
@application.route('/contact-success')
def get_contact_success_page():
    return render_template('contact-success.html', current_year=year)


# Takes in contact form data from contact.html to send to administrator's email
@application.route('/submit', methods=['POST'])
def get_form_sent():
    if request.method == 'POST':
        contact_name = request.form['contact-name']
        contact_email = request.form['contact-email']
        category = request.form['category']
        message = request.form['message']
        email_message(contact_name, contact_email, message, category)
        email_message(contact_name, contact_email, message, category, recipient_email="mod.vcresourcecenter@gmail.com")
    return application.redirect('/contact-success')


# a route for the footer on any html page to go to in order to send a notification that someone has signed up for the
# newsletter.
@application.route('/sign-up', methods=['POST'])
def newsletter_signup():
    name = request.form['name']
    email = request.form['email']
    email_message(name, email)
    email_message(name, email, recipient_email="mod.vcresourcecenter@gmail.com")
    return redirect('/')



# gets the post selected data and displays it as a full page
@application.route('/post')
def get_full_post():
    events_json = requests.get('https://api.npoint.io/a0fbacdbf8f5e6a731a3').json()
    id_num = int(request.args["id_num"])
    post_data: dict = {}
    for post in events_json:
        if id_num == post["id"]:
            post_data = post
    return render_template('full-post.html', post_data=post_data, current_year=year)


@application.route('/donate')
def get_donation_page():
    return render_template('donations.html', current_year=year)


if __name__ == "__main__":
    application.run(debug=True)
