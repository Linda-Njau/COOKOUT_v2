from app.models import Tag
from app import db


class TagService:
    def get_all_tags(self):
        """Returns all tags in the database"""
        tags = Tag.query.all()

        tag_list = []
        for tag in tags:
            tag_data = {
                'id': tag.id,
                'name': tag.name
            }
            tag_list.append(tag_data)

        return tag_list

    def get_tag(self, tag_id):
        tag = Tag.query.get(tag_id)
        if not tag:
            return {'error': 'tag not found'}, 404

        tag_data = {
            'id': tag.id,
            'name': tag.name
        }
        return tag_data
