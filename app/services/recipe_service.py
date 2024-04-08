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
        tags = data.get('tags', [])
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
        if tags:  
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
        print("Recipe type:", type(recipe))
        print("Recipe details:", recipe)
        return recipe.serialize(), 200
    
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
            return {'error': 'recipe not found'}, 404
        
        tags = recipe.tags

        db.session.delete(recipe)
        db.session.commit()
        
        for tag in tags:
            if not tag.recipes:
                db.session.delete(tag)
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
