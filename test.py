import socket
from werkzeug.security import generate_password_hash
from extensions import db

print(db.admins.find_one({"user_id": 1}))
