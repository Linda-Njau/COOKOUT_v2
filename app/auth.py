from flask import Blueprint, request, jsonify
from models import User
from app import db
from flask_jwt_extended import create_access_token
auth = Blueprint('auth', __name__)

def get_error_message(errors, status_code):
    """
    Create a standardized error response.
    
    Args:
        errors (dict): A dictionary of error messages.
        status_code (int): The HTTP status code associated with the error.

    Returns:
        dict: A dictionary containing the error message(s) and the corresponding status code.
    """
    return {'errors': errors}, status_code

@auth.route('/login', methods=['POST'])
def login():
   username = request.json.get("username", None)
   password = request.json.get("password", None)
   
   error_messages = {}
   
   if not username:
        error_messages['usernameError'] = "Please provide a username"
   if not password:
        error_messages['passwordError'] = "Please provide a password"
    
   if error_messages:
        return get_error_message(error_messages, 400)
   
   user = User.query.filter_by(username=username).first()
   
   if user is None or not user.check_password(password):
       return get_error_message({"loginError": "Invalid username or password"}, 401)
   access_token = create_access_token(identity=username)
   return jsonify(access_token=access_token, user_id=user.id), 200
