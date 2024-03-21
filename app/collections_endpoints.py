from flask import Blueprint, request, jsonify
from models import Collection
from app import db
from app.services.collection_service import CollectionService

collections = Blueprint('collections', __name__)
collection_service = CollectionService()


@collections.route('/collections', methods=['GET'], strict_slashes=False)
def get_all_collections():
    """Returns all collections"""
    recipe_collections = collection_service.get_all_collections()
    return jsonify(recipe_collections)


@collections.route('/collections/<int:collection_id>', methods=['GET'], strict_slashes=False)
def get_collection(collection_id):
    """Get collection by id"""
    collection = collection_service.get_collection(collection_id)
    return jsonify(collection)
