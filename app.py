from flask import Flask, jsonify, request
from flask_migrate import Migrate  
from models import db, Episode, Guest, Appearance

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Routes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes])


@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode_by_id(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    episode_dict = episode.to_dict()
    episode_dict['appearances'] = [appearance.to_dict() for appearance in episode.appearances]
    return jsonify(episode_dict)


@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests])


@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()

    try:
        rating = int(data.get("rating"))
        episode_id = data.get("episode_id")
        guest_id = data.get("guest_id")

        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        if not episode_id or not guest_id:
            raise ValueError("Episode ID and Guest ID are required")

        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)
        if not episode or not guest:
            raise ValueError("Guest or Episode not found")

        appearance = Appearance(
            rating=rating,
            episode_id=episode_id,
            guest_id=guest_id
        )

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

    except Exception :
        return jsonify({"errors": ["validation errors"]}), 400


if __name__ == '__main__':
    app.run(debug=True)