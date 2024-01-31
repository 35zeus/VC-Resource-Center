import socket
from werkzeug.security import generate_password_hash
from extensions import db

print(list(db.events.find().sort([('timestamp', -1)]).limit(1))[0]["post_id"])
