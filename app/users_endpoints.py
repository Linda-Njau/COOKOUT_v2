from flask import Blueprint, request, jsonify
from models import User
from app import db
from app.services.user_service import UserService

users = Blueprint('users', __name__)
user_service = UserService()

@users.route('/users', methods=['GET'])
def get_users():
    all_users = user_service.get_users()
    return jsonify(all_users), 200

@users.route('/users/<int:user_id>/recipes', methods=['GET'])
def get_user_recipes(user_id):
    user_recipes, status_code = user_service.get_user_recipes(user_id)
    return jsonify(user_recipes), status_code

@users.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user"""
    data = request.get_json()
    response, status_code = user_service.create_user(data)
    return jsonify(response), status_code


@users.route('/users/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user, status_code = user_service.get_user(user_id)
    return jsonify(user), status_code

@users.route('/users/<string:username>', methods=['GET'], strict_slashes=False)
def get_user_by_username(username):
    user, status_code = user_service.get_user_by_username(username)
    return jsonify(user), status_code

@users.route('/users/<int:user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    data = request.get_json()
    response = user_service.update_user(user_id, data)
    return jsonify(response), 200


@users.route('/users/<int:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    response = user_service.delete_user(user_id)
    return jsonify(response), 200

@users.route('/users/<user_id>/follow', methods=['POST'], strict_slashes=False)
def follow_user(user_id):
    data = request.get_json()
    response, status_code = user_service.follow_user(data, user_id)
    return jsonify(response), status_code

@users.route('/users/<user_id>/unfollow', methods=['POST'], strict_slashes=False)
def unfollow(user_id):
    data = request.get_json()
    response, status_code = user_service.unfollow_user(data, user_id)
    return jsonify(response), status_code

@users.route('/users/<int:user_id>/is_following/<int:target_user_id>', methods=['GET'], strict_slashes=False)
def is_following(user_id, target_user_id):
    response, status_code = user_service.check_is_following(user_id, target_user_id)
    return jsonify(response), status_code

@users.route('/users/<user_id>/followed_recipes', methods=['GET'], strict_slashes=False)
def get_followed_recipes(user_id):
    recipes = user_service.get_followed_recipes(user_id)
    return recipes
