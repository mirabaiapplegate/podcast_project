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
    image_url = db.Column(db.String(200), nullable=True)
    link = db.Column(db.String(200), nullable=True)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.podcast_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event event_id=%s start_at=%s>" % (self.event_id, self.start_at)

    def __init__(self, start_at, end_at, image_url, link, podcast_id):
        """Construct Event objects"""
             
        self.start_at = start_at
        self.end_at = end_at
        self.image_url = image_url
        self.link = link
        self.podcast_id = podcast_id


class Comment(db.Model):
    """Comments of podcast website."""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment = db.Column(db.String(1000), nullable=True)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.podcast_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    #Define relationship to an user
    user = db.relationship("User",
                            backref=db.backref("comments", order_by=comment_id))

    #Define relationship to a podcast
    podcast = db.relationship("Podcast",
                            backref=db.backref("comments", order_by=comment_id))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event comment_id=%s comment=%s>" % (self.comment_id, self.comment)

    def __init__(self, comment, podcast_id, user_id):
        """Construct Comment objects"""
             
        self.comment = comment
        self.podcast_id = podcast_id
        self.user_id = user_id


class User(db.Model):
    """Users of podcast website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    profile_image = db.Column(db.String(200), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    facebook = db.Column(db.String(200), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s name=%s>" % (self.user_id, 
                self.name)

    def __init__(self, profile_image, name, facebook):
        """Construct User objects"""
             
        self.profile_image = profile_image
        self.name = name
        self.facebook = facebook

     
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
