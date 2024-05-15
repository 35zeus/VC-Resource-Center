from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, BaseView
from forms import UserForm
from flask_login import current_user, login_user, logout_user
from flask import redirect, url_for
from forms import LoginForm, PostForm
from extensions import db, BUCKET
from utils import upload_file_to_s3
import pdf2image
from PIL import Image
from tempfile import TemporaryFile


class CustomIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(CustomIndexView, self).index()

    @expose('/login', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = form.get_user()
            login_user(user)
            return super(CustomIndexView, self).index()

        if current_user.is_authenticated:
            return super(CustomIndexView, self).index()
        return self.render('login.html', form=form)


class LogoutView(BaseView):
    @expose('/', methods=['GET'])
    def index(self):
        logout_user()
        return redirect('/')


class EventView(ModelView):
    form = PostForm
    column_editable_list = ['title', 'date', 'content_body', 'content_body_post',
                            'alt',  'hours', 'address_url', 'address', 'vendors_needed', 'vendor_files']

    def on_model_change(self, form, model, is_created):
        if not is_created:
            return
        model.pretty_date = model.date.strftime('%B %d, %Y')
        file = form.image.data
        image = (
            pdf2image.convert_from_bytes(file.read())[0]
            if file.mimetype == "application/pdf"
            else Image.open(file)
        )
        image.resize((300, 400))
        temp = TemporaryFile()
        image.save(temp, "PNG")
        temp.seek(0)
        model.image = upload_file_to_s3(file=temp, bucket=BUCKET, key=f'website-pictures/{file.filename}')
        temp.close()
        if model.pretty_date and model.image:
            db.session.commit()
        else:
            print("Didn't work.")

    def is_accessible(self):
        return current_user.is_authenticated


class UserView(ModelView):
    # form_columns = ["role", "username", "password"]
    form = UserForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'


class ClickView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
