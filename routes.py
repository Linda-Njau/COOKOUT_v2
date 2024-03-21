from flask import Flask
from api.users_api import users_api
from api.recipes import recipes_api
from api.tags import tags_api
from api.collections import collections_api

app = Flask(__name__)

app.register_blueprint(users_api, url_prefix='/api/users')
app.register_blueprint(recipes_api, url_prefix='/api/recipes')
app.register_blueprint(tags_api, url_prefix='/api/tags')
app.register_blueprint(collections_api, url_prefix='/api/collections')

if __name__ == '__main__':
    app.run()
