from app import create_app, db  # Import create_app and db
from models import Episode, Guest, Appearance
from faker import Faker

fake = Faker()

# Create the app instance
app = create_app()

# Run the seeding script inside the Flask app context
with app.app_context():  # Ensure you are working inside the Flask app context
    db.create_all()  # Create the tables if they don't exist

    # Generate 10 fake episodes
    episodes = []
    for _ in range(10):
        episode_date = fake.date_this_century()
        episode = Episode.query.filter_by(date=episode_date).first()  # Check if episode exists
        if not episode:
            episode = Episode(date=episode_date, number=fake.random_int(min=1, max=100))
            db.session.add(episode)
        episodes.append(episode)

    db.session.commit()  # Commit the new episodes

    # Generate 10 fake guests
    guests = []
    for _ in range(10):
        guest = Guest(name=fake.name(), occupation=fake.job())
        db.session.add(guest)
        guests.append(guest)

    db.session.commit()  # Commit the new guests

    # Create appearances for guests
    for _ in range(20):
        appearance = Appearance(
            rating=fake.random_int(min=1, max=5),
            episode_id=fake.random_element(elements=[e.id for e in episodes]),
            guest_id=fake.random_element(elements=[g.id for g in guests])
        )
        db.session.add(appearance)

    db.session.commit()  # Commit the new appearances
    print("Database seeded successfully")
