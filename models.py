from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
recipe_tags = db.Table(
    'recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)
class Recipe(db.Model):
    """Recipe object for cookout."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    ingredients = db.Column(db.String(10000))
    instructions = db.Column(db.String(10000))
    preparation_time = db.Column(db.Integer)
    cooking_time = db.Column(db.Integer)
    calories = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    tags = db.relationship('Tag', secondary=recipe_tags, backref=db.backref('recipes', lazy='dynamic'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    hidden = db.Column(db.Boolean, default=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Collection(db.Model):
    """Collection model for grouping recipes"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    recipes = db.relationship('Recipe', backref='collection')
    
    def __repr__(self):
        return self.name
    
class Tag(db.Model):
    """ Tag object for recipes """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
class User(db.Model, UserMixin):
    """User object for cookout"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    recipes = db.relationship('Recipe')
    
    """ defining the following and followed self-referencial relationship between User objects """
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

def follow(self, user):
    """Follow function for User object"""
    if not self.is_following(user):
        self.followed.append(user)
        
def unfollow(self, user):
    """Unfollow function for User object"""
    if self.is_following(user):
        self.followed.remove(user)
        
def is_following(self, user):
    """Check if User object is following a user"""
    return self.followed.filter(
        followers.c.followed_id == user.id).count() > 0

def followed_recipe(self):
    """Returns recipe information of followed users or user's own"""
    followed = Recipe.query.join(
        followers, (followers.c.followed_id == Recipe.user_id)).filter(
            followers.c.follower_id == self.id)
    own = Recipe.query.filter_by(user_id==self.id)
    return followed.union(own).order_by(Recipe.date.desc())
