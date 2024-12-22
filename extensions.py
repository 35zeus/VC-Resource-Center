import os
import sshtunnel
from flask_sqlalchemy import SQLAlchemy

mod_email_password = os.getenv("MOD_EMAIL_PASSWORD")
mod_email = os.getenv("MOD_EMAIL")
recipient_email = os.getenv("RECIPIENT_EMAIL")
BUCKET = os.getenv("S3_BUCKET")
ssh_password = os.getenv("SSH_PASSWORD")
sshtunnel.SSH_TIMEOUT = 10.0
sshtunnel.TUNNEL_TIMEOUT = 10.0

# with sshtunnel.SSHTunnelForwarder(
#     ("ssh.pythonanywhere.com"),
#     ssh_username="vcresourcecenter",
#     ssh_password=ssh_password,
#     remote_bind_address=("vcresourcecenter.mysql.pythonanywhere-services.com", 3306),
# ) as tunnel:
db = SQLAlchemy()

links = {
    "99.3 Radio": "https://99threefm.com/",
    "All Saints Episcopal Church": "https://www.allsantos.org/",
    "Bethel Oxnard Church": "https://www.facebook.com/betheloxnardchurch/",
    "HDFC": "https://m.facebook.com/p/His-Dream-Fulfilled-Center-100064865103425/",
    "New Progressive Church": "https://newprogressivechristianbaptistchurch.org/",
    "CG Law": "https://cynthialgonzalezlaw.com/",
    "Faith Mission Christian Fellowship Church": "https://faithmissioncfc.org/index.html",
    "Grace Life Church": "https://www.gracechurch.org/gracelife",
    "New Directions": "https://www.google.com/search?q=new+directions&client=ubuntu&hs=34t&sca_esv=592717629&channel=fs&sxsrf=AM9HkKmI5XOsBb8a8_bvFpkOjen3ZtF79w%3A1703131784941&ei=iLqDZeaMOb3dkPIPmd-OaA&ved=0ahUKEwjm8K-o1J-DAxW9LkQIHZmvAw0Q4dUDCBA&uact=5&oq=new+directions&gs_lp=Egxnd3Mtd2l6LXNlcnAiDm5ldyBkaXJlY3Rpb25zMgoQIxiABBiKBRgnMg4QLhiABBjHARivARiOBTILEC4YgAQYxwEYrwEyERAuGIMBGMcBGLEDGNEDGIAEMgsQLhiABBjHARivATIKEAAYgAQYigUYQzILEC4YgAQYxwEYrwEyCBAAGIAEGLEDMgsQLhiABBjHARjRAzIFEAAYgARIzlBQxAJY7wlwAXgBkAEBmAHdAaABhweqAQUwLjUuMbgBA8gBAPgBAcICChAAGEcY1gQYsAPCAgYQABgWGB7CAggQABgWGB4YCuIDBBgAIEGIBgGQBgg&sclient=gws-wiz-serp",
    "Oxnard Family Circle": "https://oxnardfamilycircle.com/",
    "Zion Living World Ministries": "https://zlwm.org/",
    "Miracle Center of Ventura": "https://www.miraclecenterventura.org/",
    "California Rural Legal Assistance, Inc.": "https://crla.org/locations/oxnard",
    "Kids and Families Together": "https://www.kidsandfamilies.org/",
    "Point of Love Foundation": "https://www.pointoflove.org/gallery",
    "James Storehouse": "https://www.jamesstorehouse.org/",
}
