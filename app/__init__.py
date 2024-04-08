from flask import Flask
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    
    from .users_endpoints import users
    from .recipes_endpoints import recipes
    from .tags_endpoints import tags
    from .collections_endpoints import collections
    from .auth import auth
    
    app.register_blueprint(users)
    app.register_blueprint(recipes)
    app.register_blueprint(tags)
    app.register_blueprint(collections)
    app.register_blueprint(auth)
    
    from models import User, Recipe
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    with app.app_context():
        create_database(app)
    
    return app

def create_database(app):
    """Create a new database if it doesn't already exist"""
    if not path.exists('cookout/' + DB_NAME):
        db.create_all()
        print('Database created successfully')
