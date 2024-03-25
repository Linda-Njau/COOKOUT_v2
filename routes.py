from flask import Flask
from app.users_endpoints import users
from app.recipes_endpoints import recipes
from app.tags_endpoints import tags
from app.collections_endpoints import collections

app = Flask(__name__)

app.register_blueprint(users, url_prefix='/api/users')
app.register_blueprint(recipes, url_prefix='/api/recipes')
app.register_blueprint(tags, url_prefix='/api/tags')
app.register_blueprint(collections, url_prefix='/api/collections')

if __name__ == '__main__':
    app.run()
