from flask import Blueprint, request, jsonify
from models import Tag
from app import db
from app.services.tag_service import TagService

tags = Blueprint('tags', __name__)
tag_service = TagService()


@tags.route('/tags', methods=['GET'], strict_slashes=False)
def get_all_tags():
    """Returns all tags in the database"""
    tags = tag_service.get_all_tags()
    return jsonify(tags)


@tags.route('/tags<int:tag_id>', methods=['GET'], strict_slashes=False)
def get_tag(tag_id):
    tag = tag_service.get_tag(tag_id)
    return jsonify(tag) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    