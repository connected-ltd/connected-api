from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# App Config
app = Flask(__name__, )
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
JWTManager(app)

# Celery
from app.celery import make_celery
celery = make_celery(app)

# Database
from config import secret
app.secret_key = secret
migrate = Migrate(app, db)


# Controllers
from app.user.controller import bp as user_bp
app.register_blueprint(user_bp)
from app.files.controller import bp as files_bp
app.register_blueprint(files_bp)
from app.shortcodes.controller import bp as shortcodes_bp
app.register_blueprint(shortcodes_bp)
from app.shortcode_files.controller import bp as shortcode_files_bp
app.register_blueprint(shortcode_files_bp)
from app.messages.controller import bp as messages_bp
app.register_blueprint(messages_bp)
from app.numbers.controller import bp as numbers_bp
app.register_blueprint(numbers_bp)
from app.areas.controller import bp as areas_bp
app.register_blueprint(areas_bp)
from app.ussd.controller import bp as ussd_bp
app.register_blueprint(ussd_bp)

# Error handlers
from .error_handlers import *