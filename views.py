from flask_admin.contrib.pymongo.view import ModelView
from forms import UserForm
from werkzeug.security import generate_password_hash


class UserView(ModelView):
    column_list = ["name", "hash", "_id"]
    form_columns = ["username", "password"]
    form = UserForm

    def on_model_change(self, form, model, is_created):
        if is_created:
            model["hash"] = generate_password_hash(form.hash.data)





