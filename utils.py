from smtplib import SMTP
from extensions import (mod_email_password, mod_email, recipient_email)
import datetime
import boto3


# The following function takes env variables of the moderators email credentials, formats an email to the correct
# recipient and sends the email.
def email_message(
        name, contact_email,
        body='New Sign up for the newsletter',
        category='Newsletter',
        to_email=None
):

    if to_email is None:
        to_email = recipient_email

    with SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=mod_email, password=mod_email_password)
        connection.sendmail(
            from_addr=mod_email,
            to_addrs=to_email,
            msg=f'Subject:Contact Form Submission\n\nFrom: {name} at {contact_email}\n'
                f'Category: {category}\n'
                f'Message: {body}',
        )


def add_event_post(db, form_dict, last_post_id):
    db.events.insert_one(
        {
            "post_id": last_post_id + 1,
            "title": form_dict["post-title"],
            "date": datetime.datetime.now(),
            "pretty_date": datetime.datetime.now().strftime("%B %d, %Y"),
            "content_body": form_dict["post-subtitle"],
            "content_body_post": form_dict["ckeditor"],
            "image": f"https://elasticbeanstalk-us-west-1-124449841478.s3.us-west-1.amazonaws.com/website-pictures/{form_dict['post-image']}",
            "alt": form_dict["post-image-alt"],
            "address_url": form_dict["address-url"],
            "address": form_dict["post-address"],
            "vendors_needed": bool(form_dict['vendor-needed']),
            "vendor_files": "images/Event-12-9-23.zip",
        }
    )


def upload_file_to_s3(file_path, bucket_name=None, key_name=None, region_name=None):
    s3 = boto3.resource('s3', region_name=region_name)
    bucket = s3.Bucket(bucket_name)

    try:
        bucket.upload_file(Filename=file_path, Key=key_name)
        return "success"
    except Exception as e:
        return {"failure": e}
