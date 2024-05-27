from flask_api import status
from models import Recipe, Tag, User
from app import db

def get_error_message(errors, status_code):
    """
    Create a standardized error response.
    
    Args:
         errors (dict): A dictionary of error messages.
        status_code (int): The HTTP status code associated with the error.

    Returns:
        dict: A dictionary containing the error message(s) and the corresponding status code.
    """
    return{'errors': errors}, status_code
class RecipeService:
    def get_all_recipes(self, tags=None):
        """Retrieves all recipes"""
        if tags:
            tag_list = tags.split(',')
            recipes = Recipe.get_recipes_by_tags(tag_list)    
            
        else:
            recipes = Recipe.get_recipes_by_date()
        
        if not recipes:
            return get_error_message({'recipeError': 'No recipes found'}, status.HTTP_404_NOT_FOUND)
            
        return recipes, status.HTTP_200_OK

    def create_recipe(self, data):
        """Create a recipe from the specified attributes."""
        title = data.get('title')
        ingredients = data.get('ingredients')
        instructions = data.get('instructions')
        preparation_time = data.get('preparation_time')
        cooking_time = data.get('cooking_time')
        calories = data.get('calories')
        servings = data.get('servings')
        hidden = data.get('hidden')
        collection_id = data.get('collection_id')
        tags = data.get('tags', [])
        user_id = data.get('user_id')
        
        if not title:
            return get_error_message({'recipeError': 'No title provided'}, status.HTTP_400_BAD_REQUEST)
        
        if not user_id:
            return get_error_message({'userError': 'No user ID provided'}, status.HTTP_400_BAD_REQUEST)
        
        if tags:
            if not isinstance(tags, list):
                tags = [tags]
        
        with db.session() as session:
            user = session.get(User, user_id)
        if not user:
            return get_error_message({'userError': 'No user found'}, status.HTTP_404_NOT_FOUND)
            

        new_recipe = Recipe(
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            preparation_time=preparation_time,
            cooking_time=cooking_time,
            calories=calories,
            servings=servings,
            hidden=hidden,
            collection_id=collection_id,
            user_id=user_id
            
        )
        if tags:  
            existing_tags = Tag.query.filter(Tag.name.in_(tags)).all()
            new_tags = [Tag(name=tag_name) for tag_name in tags if tag_name not in [tag.name for tag in existing_tags]]
            new_recipe.tags.extend(existing_tags + new_tags)

        db.session.add(new_recipe)
        db.session.commit()

        return new_recipe.id, status.HTTP_201_CREATED

    def get_recipe(self, recipe_id):
        """Gets a recipe by its id."""
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return get_error_message({'recipeError': 'No recipe found'}, status.HTTP_404_NOT_FOUND)
        
        recipe_data = self._map_recipe_to_dict(recipe)
        return recipe_data, status.HTTP_200_OK

    def update_recipe(self, recipe_id, data):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return get_error_message({'recipeError': 'No recipe found'}, status.HTTP_404_NOT_FOUND)
        allowed_attributes = [
            'title', 'ingredients', 'instructions', 'preparation_time',
            'cooking_time', 'calories', 'servings', 'hidden', 'collection_id', 'tags'
        ]
        for attr, value in data.items():
            if attr in allowed_attributes:
                if attr == 'tags':
                    recipe.tags = self._handle_tags(value)
                else:
                    setattr(recipe, attr, value)

        db.session.commit()
        return recipe.serialize(), status.HTTP_200_OK
    
    def _handle_tags(self, tag_names):
        tags = []
        if isinstance(tag_names, str):
            tag_names = [tag_names]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            tags.append(tag)
        return tags

    def delete_recipe(self, recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return get_error_message({'recipeError': 'No recipe found'}, status.HTTP_404_NOT_FOUND)
        
        tags = recipe.tags

        db.session.delete(recipe)
        db.session.commit()
        
        for tag in tags:
            if not tag.recipes:
                db.session.delete(tag)
        db.session.commit()

        return {'message': 'recipe deleted successfully.'}, status.HTTP_200_OK

    def _map_recipe_to_dict(self, recipe):
        return {
            'id': recipe.id,
            'title': recipe.title,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'preparation_time': recipe.preparation_time,
            'cooking_time': recipe.cooking_time,
            'calories': recipe.calories,
            'servings': recipe.servings,
            'hidden': recipe.hidden,
            'collection': recipe.collection.name if recipe.collection else None,
            'tags': [tag.name for tag in recipe.tags],
            'user_id': recipe.user_id
        }
