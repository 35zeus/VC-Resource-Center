from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import os

load_dotenv()
mod_email_password = os.getenv('MOD_EMAIL_PASSWORD')
mod_email = os.getenv('MOD_EMAIL')
recipient_email = os.getenv('RECIPIENT_EMAIL')
app_secretkey = os.getenv('APP_SECRET_KEY')

client = MongoClient(os.getenv('MONGODB_URI'))
db = client.event_posts
