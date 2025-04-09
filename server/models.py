from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

# Episode Model
class Episode(db.Model):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    # Relationship with appearances
    appearances = db.relationship('Appearance', backref='episode', lazy=True)

    def to_dict(self):
        """Serialize the Episode object to a dictionary"""
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'number': self.number
        }

# Guest Model
class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)

    # Relationship with appearances
    appearances = db.relationship('Appearance', backref='guest', lazy=True)

    def to_dict(self):
        """Serialize the Guest object to a dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }

# Appearance Model
class Appearance(db.Model):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    
    # Foreign keys
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    def to_dict(self):
        """Serialize the Appearance object to a dictionary"""
        return {
            'id': self.id,
            'rating': self.rating,
            'episode_id': self.episode_id,
            'guest_id': self.guest_id
        }
