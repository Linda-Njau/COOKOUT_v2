from models import User, Recipe
from app import db


class UserService:
    
    def get_users(self):
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                # Include other user attributes as needed
            }
            user_list.append(user_data)
        return user_list
    
    def create_user(self, data):
        """Create a new user"""
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        if not email or not password or not username:
            return {'error': 'missing required fields'}, 400

        new_user = User(
            email=email,
            username=username,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'Welcome to Cookout', 'user_id': new_user.id}, 201

    def get_user(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found.'}, 404

        user_data = {
            'id': user.id,
            'email': user.email,
            'username': user.username
        }
        return user_data

    def update_user(self, user_id, data):
        """update user information"""
        user = User.query.get(user_id)
        if not user:
            return {"error": 'User not found'}, 404

        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        user.email = email
        user.password = password
        user.username = username

        db.session.commit()

        return {'message': 'User updated successfully.'}

    def delete_user(self, user_id):
        """Deletes a user by their user id"""
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found.'}, 404

        db.session.delete(user)
        db.session.commit()

        return {'message': 'User deleted successfully.'}
    
    def get_user_recipes(self, user_id):
        with db.session() as session:
            user = session.get(User, user_id)
        if not user:
            return {'error': 'User not found'}
        
        user_recipes = Recipe.query.filter_by(user_id=user_id).all()
        if user_recipes:
            serialized_recipes = [recipe.serialize() for recipe in user_recipes]
            return serialized_recipes
