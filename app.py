from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from utils.helpers import load_json_as_namedtuple

config = load_json_as_namedtuple("./app_config.json")


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gruppi.db'
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_STRING

db = SQLAlchemy(app)
migrate = Migrate(app, db)
