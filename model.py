"""Models and database functions for Podcast Storybook project."""

from flask_sqlalchemy import SQLAlchemy

# Connect to the SQLite database
db = SQLAlchemy()


##############################################################################
# Model definitions

class Podcast(db.Model):
    """Podcasts of podcast website."""

    __tablename__ = "podcasts"

    podcast_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    show = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    audio = db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(200), nullable=True)
    image_caption = db.Column(db.String(2000), nullable=True)
    
    #Define relationship to an event
    event = db.relationship("Event",
                            backref=db.backref("podcasts", order_by=podcast_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Podcast podcast_id=%s title=%s>" % (self.podcast_id, self.title)

    def __init__(self, title, show, description, audio, image, image_caption):
        """Construct Project objects"""

        self.title = title
        self.show = show
        self.description = description
        self.audio = audio
        self.image = image
        self.image_caption = image_caption
         
class Event(db.Model):
    """Events of podcast website."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    start_at = db.Column(db.Integer, nullable=False)
    end_at = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(200), nullable=True)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.podcast_id'))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event event_id=%s start_at=%s" % (self.event_id, self.start_at)

    def __init__(self, event_id, start_at, end_at, url, podcast_id):
        """Construct Event objects"""
             
        self.event_id = event_id
        self.start_at = start_at
        self.end_at = end_at
        self.url = url
        self.podcast_id = podcast_id
         

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///podcasts.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."