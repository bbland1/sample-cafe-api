import secrets
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##Cafe TABLE Configuration
class Cafe(db.Model):
    __tablename__ = "London Cafes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    black_coffee_price = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f'<Cafe: ID: {self.id} NAME: {self.name} LOCATION: {self.location}>'
    
    # make calls to dictionary
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'map_url': self.map_url,
            'img_url': self.img_url,
            'location': self.location,
            'seats': self.seats,
            'has_toilet': self.has_toilet,
            'has_wifi': self.has_wifi,
            'has_sockets': self.has_sockets,
            'can_take_calls': self.can_take_calls,
            'black_coffee_price': self.black_coffee_price,
        }
    
# model for an api key database that will generate a secret api key as a user is made
class APIUsers(db.Model):
    __tablename__ = "api_keys"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    api_key = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f'<APIUser: ID: {self.id} USER: {self.username}>'

    # generating a secret api key for a user
    def __init__(self, username):
        self.username = username
        self.api_key = secrets.token_hex(16)
        db.session.add(self)
        db.session.commit()