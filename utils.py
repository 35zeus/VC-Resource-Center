from smtplib import SMTP
from extensions import (mod_email_password, mod_email, recipient_email)


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
