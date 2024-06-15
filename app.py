from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from utils.helpers import load_env_config

config = load_env_config()
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gruppi.db'
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_STRING

db = SQLAlchemy(app)
migrate = Migrate(app, db)
