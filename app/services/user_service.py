from werkzeug.security import generate_password_hash
import re
from models import User, Recipe
from app import db


def get_error_message(errors, status_code):
    """
    Create a standardized error response.
    
    Args:
        errors (str or list): A single error message or a list of error messages.
        status_code (int): The HTTP status code associated with the error.

    Returns:
        dict: A dictionary containing the error message(s) and the corresponding status code.
    """
    if isinstance(errors, list):
        error_message = '; '.join(errors)
    else:
        error_message = errors
    return{'error': error_message}, status_code
        
class UserService:
    def is_valid_user(self, data, context):
        """
        Validates user data based on the specified context ('create' or 'update').

        Args:
            data (dict): The data dictionary containing user information.
            context (str): The context in which the validation is being performed ('create' or 'update').

        Returns:
            tuple: A tuple containing a boolean indicating validity and a list of error messages, if any.
        """
        error_messages = []
        if context == 'create':
            if 'email' not in data:
                error_messages.append("Please provide a valid email address")
            else:
                if not self.is_valid_format(data['email']):
                    error_messages.append("Invalid email format")
                if self.is_email_taken(data['email']):
                    error_messages.append("Email address already in use")
            
            if 'password' not in data:
                error_messages.append("please provide a password")
            elif len(data['password']) < 8:
                error_messages.append("Password must be at least 8 characters")
            
            if 'username' not in data:
                error_messages.append("Please provide a username")
            else:
                if self.is_username_taken(data['username']):
                    error_messages.append("Username already in use")
        
        if error_messages:
            return False, error_messages
        return True, None
    
    def is_username_taken(self, username):
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return existing_user is not None
    
    def is_valid_format(self, email):
        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return re.match(email_regex, email) is not None
            
    def is_email_taken(self, email):
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return existing_user is not None
        
    def get_users(self):
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
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
    
    def get_user_by_username(self, username):
        user = User.query.filter_by(username=username).first()
        print(user)
        if not user:
            return{'error': 'User not found'}, 404
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
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

    def follow_user(self, data, user_id):

        followed_id = data.get('followed_id')
        
        with db.session() as session:
            follower = session.get(User, user_id)
            followed = session.get(User, followed_id)
        
            if not follower: 
                return {'error': 'Invalid follower'}
            
            if not followed: 
                return {'error': 'Invalid followed'}
            
            follower.follow(followed)
            
            new_followed_count = follower.count_followed()
            all_followed = follower.all_followed()
            print(all_followed)
            db.session.commit()
        
        
        return {'message': 'You are now following this user'}, new_followed_count
    
    
    def unfollow_user(self, data, user_id):

        followed_id = data.get('followed_id')
        
        with db.session() as session:
            follower = session.get(User, user_id)
            followed = session.get(User, followed_id)
            
            if not follower:
                return {'error': 'Invalid follower'}
            
            if not followed:
                return {'error': 'Invalid followed'}
                
            follower.unfollow(followed)
            
            new_followed_count = follower.count_followed()
        db.session.commit()
        return {'success': 'You have unfollowed this user'}, new_followed_count
    
    
    def get_followed_recipes(self, user_id):
        with db.session() as session:
            user = session.get(User, user_id)
            if not user:
                return {'error': 'User not found'}
            recipes = user.followed_recipes()
            if recipes:
                serialized_recipes = [recipe.serialize() for recipe in recipes]
                return serialized_recipes
        return None

    def check_is_following(self, user_id, target_user_id):
        with db.session() as session:
            user = session.get(User, user_id)
            target_user = session.get(User, target_user_id)
            if not user:
                return {'Error': 'User not found'}
            if not target_user:
                return {'Error': 'Target user not found'}
            is_following = user.is_following(target_user)
        return is_following
