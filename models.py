from extensions import db
from sqlalchemy import event
from werkzeug.security import generate_password_hash
from datetime import datetime as dt


class AnnualType:
    def __init__(self, month: str, iterration: str, day_of_week: str):
        self.month: str = month
        self.iterration: str = iterration
        self.day_of_week: str = day_of_week

    def __str__(self):
        return f"{self.iterration}, {self.day_of_week}, {self.month}"

    def __repr__(self):
        return f"AnnualDay({self.iterration} {self.day_of_week} of {self.month})"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    pretty_date = db.Column(db.String, nullable=False)
    content_body = db.Column(db.Text)
    content_body_post = db.Column(db.Text)
    image = db.Column(db.Text, nullable=False)
    alt = db.Column(db.String, nullable=False)
    hours = db.Column(db.String)
    address_url = db.Column(db.String)
    address = db.Column(db.String)
    vendors_needed = db.Column(db.String, nullable=False)
    vendor_files = db.Column(
        db.String,
        nullable=False,
        default="documents/Ventura County Resource Center Vendor application rev.2 (1).pdf"
    )

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    created = db.Column(db.DateTime, default=dt.now)
    last_logged_in = db.Column(db.DateTime, default=dt.now)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    return generate_password_hash(value) if value != oldvalue else value


class SponsorClick(db.Model):
    __tablename__ = 'sponsor_click'
    id = db.Column(db.Integer, primary_key=True)
    sponsor_link = db.Column(db.String)
    link_clicked = db.Column(db.DateTime, default=dt.now)


class AnnualEvent(db.Model):
    __tablename__ = 'annual_event'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String, nullable=False)
    individual_posts = db.relationship('AnnualEventPost', back_ref='annual_event', lazy=False)
    last_updated = db.Column(db.DateTime)
    last_email = db.Column(db.DateTime)
    usual_date = db.Column(db.String)

    def __repr__(self):
        return f"Annual Event('{self.event_name}')"


class AnnualEventPost(db.Model):
    __tablename__ = 'annual_event_posts'
    annual_event_id = db.Column(db.String, db.ForeignKey('annual_event.id'))
    annual_event_name = db.Column(db.String, db.ForeignKey('annual_event.event_name'))
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    pretty_date = db.Column(db.String, nullable=False)
    content_body = db.Column(db.Text)
    content_body_post = db.Column(db.Text)
    image = db.Column(db.Text, nullable=False)
    alt = db.Column(db.String, nullable=False)
    hours = db.Column(db.String)
    address_url = db.Column(db.String)
    address = db.Column(db.String)
    vendors_needed = db.Column(db.String, nullable=False, default=False)
    vendor_files = db.Column(
        db.String,
        nullable=False,
        default="documents/Ventura County Resource Center Vendor application rev.2 (1).pdf"
    )

    def __repr__(self):
        return f"AnnualEventPost('{self.annual_event_name}', '{self.date}')"


