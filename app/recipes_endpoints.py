from flask import Blueprint, jsonify, request
from models import Recipe, Tag
from app import db
from app.services.recipe_service import RecipeService

recipes = Blueprint('recipes', __name__)
recipe_service = RecipeService()

@recipes.route('/recipes', methods=['GET'], strict_slashes=False)
def get_recipes():
    """Retrieves all recipes"""
    tags = request.args.get('tags')
    user_recipes = recipe_service.get_all_recipes(tags)
    return jsonify(user_recipes)


@recipes.route('/recipes', methods=['POST'], strict_slashes=False)
def create_recipe():
    """Create a recipe from the specified attributes."""
    data = request.get_json()
    response = recipe_service.create_recipe(data)
    return jsonify(response)


@recipes.route('/recipes/<int:recipe_id>', methods=['GET'], strict_slashes=False)
def get_recipe(recipe_id):
    """Gets a recipe by its id."""
    recipe = recipe_service.get_recipe(recipe_id)
    return jsonify(recipe)


@recipes.route('/recipes/<int:recipe_id>', methods=['PUT'], strict_slashes=False)
def update_recipe(recipe_id):
    data = request.get_json()
    response = recipe_service.update_recipe(recipe_id, data)
    return jsonify(response)


@recipes.route('/recipes/<int:recipe_id>', methods=['DELETE'], strict_slashes=False)
def delete_recipe(recipe_id):
    response = recipe_service.delete_recipe(recipe_id)
    return jsonify(response)
