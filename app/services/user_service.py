from werkzeug.security import generate_password_hash
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
        password_hash = generate_password_hash(password)

        if not email or not password or not username:
            return {'error': 'missing required fields'}, 400

        new_user = User(
            email=email,
            username=username,
            password_hash=password_hash
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
        if not user_id:
            return {'error': 'User not found'}
        with db.session() as session:
            user = session.get(User, user_id)
        if not user:
            return {'error': 'User not found'}
        
        user_recipes = Recipe.query.filter_by(user_id=user_id).all()
        if user_recipes:
            serialized_recipes = [recipe.serialize() for recipe in user_recipes]
            return serialized_recipes
        return None

    def follow_user(self, data):
        follower_id = data.get('follower_id')
        followed_id = data.get('followed_id')
        
        with db.session() as session:
            follower = session.get(User, follower_id)
            followed = session.get(User, followed_id)
        
            if not follower: 
                return {'error': 'Invalid follower'}
            
            if not followed: 
                return {'error': 'Invalid followed'}
            
            follower.follow(followed)
            
            new_followed_count = follower.count_followed()
        db.session.commit()
        
        
        return {'message': 'You are now following this user'}, new_followed_count
    
    
    def unfollow_user(self, data):
        follower_id = data.get('follower_id')
        followed_id = data.get('followed_id')
        
        with db.session() as session:
            follower = session.get(User, follower_id)
            followed = session.get(User, followed_id)
            
            if not follower:
                return {'error': 'Invalid follower'}
            
            if not followed:
                return {'error': 'Invalid followed'}
                
            follower.unfollow(followed)
            
            new_followed_count = follower.count_followed()
        db.session.commit()
        return {'success': 'You have unfollowed this user'}, new_followed_count
    
    
    