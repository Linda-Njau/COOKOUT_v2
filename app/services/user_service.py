from werkzeug.security import generate_password_hash
import re
from flask_api import status
from models import User, Recipe
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
        error_messages = {}
        if context == 'create':
            if not data.get('email'):
                error_messages['emailError'] = "Please provide a valid email address"
            else:
                if not self.is_valid_format(data['email']):
                    error_messages["emailError"] = "Invalid email format"
                if self.is_email_taken(data['email']):
                    error_messages["emailError"] ="Email address already in use"
            
            if  not data.get('password'):
                error_messages["passwordError"] = "please provide a password"
            elif len(data['password']) < 8:
                error_messages["passwordError"] = "Password must be at least 8 characters"
            
            if not data.get('username'):
                error_messages['usernameError'] = "Please provide a username"
            else:
                if self.is_username_taken(data['username']):
                    error_messages['usernameError'] = "Username already in use"
        if context == 'update':
            if 'email' in data:
                if not self.is_valid_format(data['email']):
                    error_messages["emailError"] = "Invalid email format"
                if self.is_email_taken(data['email']):
                    error_messages["emailError"] ="Email address already in use"
        
            if 'password' in data:
                if len(data['password']) < 8:
                    error_messages["passwordError"] = "Password must be at least 8 characters"
                
            if 'username' in data:
                if self.is_username_taken(data['username']):
                    error_messages['usernameError'] = "Username already in use"
                
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
        if not users:
             return get_error_message({'useError': 'User not found'}, status.HTTP_400_BAD_REQUEST)
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
        is_valid, errors = self.is_valid_user(data, context="create")
        
        if not is_valid:
            return get_error_message(errors, status.HTTP_400_BAD_REQUEST)
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        password_hash = generate_password_hash(password)

        new_user = User(
            email=email,
            username=username,
            password_hash=password_hash
        )
    
        db.session.add(new_user)
        db.session.commit()
        
        if new_user.id:
            return {'user_id': new_user.id}, status.HTTP_201_CREATED
        
        
    def get_user(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return get_error_message({'useError': 'User not found'}, status.HTTP_400_BAD_REQUEST)

        user_data = {
            'id': user.id,
            'email': user.email,
            'username': user.username
        }
        return user_data, status.HTTP_200_OK
    
    def get_user_by_username(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return get_error_message({'userError': 'User not found.'}, status.HTTP_400_BAD_REQUEST)
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return user_data, status.HTTP_200_OK


    def update_user(self, user_id, data):
        """update user information"""
        user = User.query.get(user_id)
        if not user:
            return get_error_message({'useError': 'User not found'}, status.HTTP_400_BAD_REQUEST)
        
        is_valid, errors = self.is_valid_user(data, context="update")
        
        if not is_valid:
            return get_error_message(errors, status.HTTP_400_BAD_REQUEST)
        
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        user.email = email
        user.password = password
        user.username = username

        db.session.commit()

        return {'message': 'User updated successfully.'}, status.HTTP_200_OK

    def delete_user(self, user_id):
        """Deletes a user by their user id"""
        user = User.query.get(user_id)
        if not user:
            return get_error_message({'userError': 'User not found.'}, status.HTTP_400_BAD_REQUEST)

        db.session.delete(user)
        db.session.commit()
        return {'message': 'user deleted succesffuly'}, status.HTTP_200_OK
    
    def get_user_recipes(self, user_id):

        with db.session() as session:
            user = session.get(User, user_id)
        if not user:
            return get_error_message({'userError': 'User not found.'}, status.HTTP_400_BAD_REQUEST)
        
        user_recipes = Recipe.query.filter_by(user_id=user_id).all()
        
        if not user_recipes:
            return get_error_message({'recipesError': 'No recipes found for this user.'}, status.HTTP_404_NOT_FOUND)
      
        serialized_recipes = [recipe.serialize() for recipe in user_recipes]
        return serialized_recipes, status.HTTP_200_OK

    def follow_user(self, data, user_id):

        followed_id = data.get('followed_id')
        
        with db.session() as session:
            follower = session.get(User, user_id)
            followed = session.get(User, followed_id)
        
            if not follower: 
               return get_error_message({'userError': 'User not found.'}, status.HTTP_400_BAD_REQUEST)
           
            if not followed: 
                return get_error_message({'userError': 'Target user not found.'}, status.HTTP_400_BAD_REQUEST)
            
            follower.follow(followed)
            
            new_followed_count = follower.count_followed()
            db.session.commit()
        
        
        return new_followed_count, status.HTTP_200_OK
    
    
    def unfollow_user(self, data, user_id):

        followed_id = data.get('followed_id')
        
        with db.session() as session:
            follower = session.get(User, user_id)
            followed = session.get(User, followed_id)
            
            if not follower:
                return get_error_message({'userError': 'User not found.'}, status.HTTP_400_BAD_REQUEST)
            
            if not followed:
                return get_error_message({'userError': 'Target user not found.'}, status.HTTP_400_BAD_REQUEST)
                
            follower.unfollow(followed)
            
            new_followed_count = follower.count_followed()
        db.session.commit()
        return new_followed_count, status.HTTP_200_OK
    
    
    def get_followed_recipes(self, user_id):
        with db.session() as session:
            user = session.get(User, user_id)
            if not user:
                return get_error_message({'userError': 'User not found.'}, status.HTTP_400_BAD_REQUEST)
            recipes = user.followed_recipes()
            if not recipes:
                return get_error_message({'recipesError': 'No recipes found.'}, status.HTTP_404_NOT_FOUND)
            
            serialized_recipes = [recipe.serialize() for recipe in recipes]
            return serialized_recipes, status.HTTP_200_OK
       

    def check_is_following(self, user_id, target_user_id):
        with db.session() as session:
            user = session.get(User, user_id)
            target_user = session.get(User, target_user_id)
            if not user:
                return get_error_message({'userError': 'User not found.'}, status.HTTP_400_BAD_REQUEST)
            if not target_user:
                return get_error_message({'userError': 'Target user not found.'}, status.HTTP_400_BAD_REQUEST)
            is_following = user.is_following(target_user)
        
        return is_following, status.HTTP_200_OK
