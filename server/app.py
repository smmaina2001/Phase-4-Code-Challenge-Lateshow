from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from models import db, Episode, Guest, Appearance

# Initialize the Flask extensions
migrate = Migrate()

# Define the create_app function
def create_app():
    # Initialize the Flask app
    app = Flask(__name__)

    # Configure the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Define the routes

    @app.route('/episodes', methods=['GET'])
    def get_episodes():
        """Fetch all episodes"""
        episodes = Episode.query.all()
        return jsonify([episode.to_dict() for episode in episodes])

    @app.route('/episodes/<int:id>', methods=['GET'])
    def get_episode_by_id(id):
        """Fetch a specific episode by its ID"""
        episode = Episode.query.get(id)
        if not episode:
            return jsonify({"error": "Episode not found"}), 404

        # If the episode exists, include its appearances as well
        episode_dict = episode.to_dict()
        episode_dict['appearances'] = [appearance.to_dict() for appearance in episode.appearances]
        return jsonify(episode_dict)

    @app.route('/guests', methods=['GET'])
    def get_guests():
        """Fetch all guests"""
        guests = Guest.query.all()
        return jsonify([guest.to_dict() for guest in guests])

    @app.route('/appearances', methods=['POST'])
    def create_appearance():
        """Create a new appearance"""
        data = request.get_json()

        try:
            # Extracting and validating the data
            rating = int(data.get("rating"))
            episode_id = data.get("episode_id")
            guest_id = data.get("guest_id")

            # Validation checks
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")
            if not episode_id or not guest_id:
                raise ValueError("Episode ID and Guest ID are required")

            # Fetch episode and guest from the database
            episode = Episode.query.get(episode_id)
            guest = Guest.query.get(guest_id)

            if not episode or not guest:
                raise ValueError("Guest or Episode not found")

            # Creating a new Appearance instance
            appearance = Appearance(
                rating=rating,
                episode_id=episode_id,
                guest_id=guest_id
            )

            # Add appearance to session and commit to the database
            db.session.add(appearance)
            db.session.commit()

            return jsonify({
                "id": appearance.id,
                "rating": appearance.rating,
                "guest_id": appearance.guest_id,
                "episode_id": appearance.episode_id,
                "episode": {
                    "id": episode.id,
                    "date": episode.date,
                    "number": episode.number
                },
                "guest": {
                    "id": guest.id,
                    "name": guest.name,
                    "occupation": guest.occupation
                }
            }), 201

        except Exception:
            return jsonify({"errors": ["validation errors"]}), 400

    return app


# Initialize the app using the create_app function
app = create_app()

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the tables if they don't exist
    app.run(debug=True)
