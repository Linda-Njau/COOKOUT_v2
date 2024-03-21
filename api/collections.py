from flask import Blueprint, request, jsonify
from app.models import Collection
from app import db
from app.api.services.collection_service import CollectionService

collections_api = Blueprint('collections_api', __name__)
collection_service = CollectionService()


@collections_api.route('/', methods=['GET'], strict_slashes=False)
def get_all_collections():
    """Returns all collections"""
    collections = collection_service.get_all_collections()
    return jsonify(collections)


@collections_api.route('/<int:collection_id>', methods=['GET'], strict_slashes=False)
def get_collection(collection_id):
    """Get collection by id"""
    collection = collection_service.get_collection(collection_id)
    return jsonify(collection)
