"""Utility file to seed podcast database from data in seed_data/"""


from model import Podcast, Event, User, connect_to_db, db
from server import app


def load_podcasts():
    """Load podcasts from u.podcast into database."""

    print "Podcasts"

    # Delete db to avoid duplicates
    Podcast.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.podcast"):
        row = row.strip()
        title, show, description, audio, image, image_caption = row.split("|")

        podcast = Podcast(title=title, show=show, description=description, 
                        audio=audio, image=image, image_caption=image_caption)

        # We need to add to the session or it won't ever be stored
        db.session.add(podcast)

    # Once we're done, we should commit our work
    db.session.commit()


def load_events():
    """Load events from u.event into database."""

    print "Events"

    # Delete db to avoid duplicates
    Event.query.delete()

    # Read u.event file and insert data
    for row in open("seed_data/u.event"):
        row = row.rstrip()

        start_at, end_at, image_url, link, podcast_id = row.split("|")

        event = Event(start_at=start_at, end_at=end_at, image_url=image_url,
                     link=link, podcast_id=podcast_id)

        # add event to session
        db.session.add(event)

    # Commit the add of an event
    db.session.commit()

def load_user():
    """Load user from u.user into database."""

    print "User"

    # Delete db to avoid duplicates
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()

        profile_image, first_name, last_name, email, password = row.split("|")

        user = User(profile_image=profile_image, first_name=first_name, last_name=last_name,
                    email=email, password=password)

        # add event to session
        db.session.add(user)

    # Commit the add of an event
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them 
    db.create_all()

    # Import different types of data
    load_podcasts()
    load_events()
    load_user()