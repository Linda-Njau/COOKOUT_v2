from models import Recipe, Tag, User
from app import db


class RecipeService:
    def get_all_recipes(self, tags=None):
        """Retrieves all recipes"""
        if tags:
            tag_list = tags.split(',')
            query = Recipe.query.filter(Recipe.hidden == False)
        
            query = query.join(Recipe.tags)
            
            query = query.filter(Tag.name.in_(tag_list))
            
            recipes = query.all()
        else:
            recipes = Recipe.query.all()
        
        serialized_recipes = [recipe.serialize() for recipe in recipes]
        return serialized_recipes

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
        tags = data.get('tags')
        user_id = data.get('user_id')

        if not title:
            return {'error': 'Your recipe needs a title'}, 400
        
        if tags:
            if not isinstance(tags, list):
                tags = [tags]
        
        with db.session() as session:
            user = session.get(User, user_id)
        if not user:
                return {'error': 'User not found'}
            

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
      
            
        existing_tags = Tag.query.filter(Tag.name.in_(tags)).all()
        new_tags = [Tag(name=tag_name) for tag_name in tags if tag_name not in [tag.name for tag in existing_tags]]
        new_recipe.tags.extend(existing_tags + new_tags)

        db.session.add(new_recipe)
        db.session.commit()

        return {'message': 'Your recipe has been created!', 'recipe_id': new_recipe.id}, 201

    def get_recipe(self, recipe_id):
        """Gets a recipe by its id."""
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return {'error': 'recipe not found'}, 404
        recipe_data = self._map_recipe_to_dict(recipe)
        return recipe_data

    def update_recipe(self, recipe_id, data):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return {'error': 'Recipe not found'}, 404

        title = data.get('title')
        ingredients = data.get('ingredients')
        instructions = data.get('instructions')
        preparation_time = data.get('preparation_time')
        cooking_time = data.get('cooking_time')
        calories = data.get('calories')
        servings = data.get('servings')
        hidden = data.get('hidden')
        collection_id = data.get('collection_id')
        tag_ids = data.get('tag_ids')

        recipe.title = title
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        recipe.preparation_time = preparation_time
        recipe.cooking_time = cooking_time
        recipe.calories = calories
        recipe.servings = servings
        recipe.hidden = hidden
        recipe.collection_id = collection_id

        if tag_ids:
            tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            recipe.tags = tags

        db.session.commit()
        return {'message': 'Recipe updated successfully'}

    def delete_recipe(self, recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return {'error': 'recipe not found'}, 404

        db.session.delete(recipe)
        db.session.commit()

        return {'message': 'recipe deleted successfully.'}

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
