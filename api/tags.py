from flask import Blueprint, request, jsonify
from app.models import Tag
from app import db
from app.api.services.tag_service import TagService

tags_api = Blueprint('tags_api', __name__)
tag_service = TagService()


@tags_api.route('/', methods=['GET'], strict_slashes=False)
def get_all_tags():
    """Returns all tags in the database"""
    tags = tag_service.get_all_tags()
    return jsonify(tags)


@tags_api.route('/<int:tag_id>', methods=['GET'], strict_slashes=False)
def get_tag(tag_id):
    tag = tag_service.get_tag(tag_id)
    return jsonify(tag) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    