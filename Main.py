from flask import Flask, render_template, redirect
import flask
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy  
from wtforms import StringField, SubmitField, PasswordField, SelectField, HiddenField
from wtforms.validators  import data_required, EqualTo
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import LoginManager, logout_user, login_user, UserMixin, login_required

login_manager = LoginManager()

# initializing Sql database
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

# initializing Flask app
app = Flask(__name__)
# Configuring flask database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = "PIFANMOPWAINFOANWOFIKNAOFKNAOWFNMO"

db.init_app(app)
login_manager.init_app(app)

#
class User(db.Model, UserMixin):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]
    def get_id(self):
        return (self.user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Using WTFforms to create a sign in form
class Sign_in_form(FlaskForm):
    username = StringField("Username:",validators=[data_required()])
    email = StringField("Email:",validators=[data_required()])
    password = PasswordField("Password:",validators=[data_required()])
    submit = SubmitField()

# Using WTFforms to create a sign up form
class Sign_up_form(FlaskForm):
    username = StringField("Username:",validators=[data_required()])
    email = StringField("Email:",validators=[data_required()])
    password = PasswordField("Password:",validators=[data_required(),EqualTo('confirm_password')])
    confirm_password = PasswordField("Confirm Password:", validators=[data_required()])
    premium = SelectField("Create a premium account?", choices=[(1,"True"),(0,"False")])
    submit = SubmitField()

@app.route("/")
@app.route("/index")
def index_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)