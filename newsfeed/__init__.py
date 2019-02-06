import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)




#########
#DATABASE#
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#######
#LOGIN CONFIGUREATION
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


from newsfeed.core.views import core
from newsfeed.users.views import users
from newsfeed.feeds.views import news_feed_b
from newsfeed.error_pages.handlers import error_pages



app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(news_feed_b)
app.register_blueprint(users)

