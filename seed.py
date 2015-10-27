"""Utility file to seed podcast database from data in seed_data/"""


from model import Podcast
from model import Event

from model import connect_to_db, db
from server import app


def load_podcasts():
    """Load podcasts from u.podcast into database."""

    print "Podcasts"

    # Delete db to avoid duplicates
    Podcast.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.podcast"):
        row = row.rstrip()
        title, episode_num, description = row.split("|")

        podcast = Podcast(title=title, episode_num=episode_num, description=description)

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
        start_at, end_at = row.split("|")

        event = Event(start_at=start_at, end_at=end_at)

    # add event to session
    db.session.add(event)

    # Commit the add of an event
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them 
    db.create_all()

    # Import different types of data
    load_podcasts()
    load_events()
