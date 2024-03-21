from models import Collection
from app import db


class CollectionService:
    def get_all_collections(self):
        """Returns all collections"""
        collections = Collection.query.all()

        collection_list = []
        for collection in collections:
            collection_data = {
                'id': collection.id,
                'name': collection.name
            }
            collection_list.append(collection_data)

        return collection_list

    def get_collection(self, collection_id):
        """Get collection by id"""
        collection = Collection.query.get(collection_id)
        if not collection:
            return {'error': 'Collection not found.'}, 404

        collection_data = {
            'id': collection.id,
            'name': collection.name
        }
        return collection_data
