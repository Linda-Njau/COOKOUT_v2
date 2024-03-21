from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .api.users import users_api
    from .api.recipes import recipes_api
    from .api.tags import tags_api
    from .api.collections import collections_api
    from .auth import auth
    
    app.register_blueprint(users_api, url_prefix='/api/users')
    app.register_blueprint(recipes_api, url_prefix='/api/recipes')
    app.register_blueprint(tags_api, url_prefix='/api/tags')
    app.register_blueprint(collections_api, url_prefix='/api/collections')

    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Recipe
    
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
