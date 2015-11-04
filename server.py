"""Podcast Storybook."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, json
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from json import dumps
from model import Podcast, Event, connect_to_db, db
import requests

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Prevent jinja from failing silently
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    podcasts = Podcast.query.all()

    return render_template("index.html", podcasts=podcasts)


@app.route('/images/<int:podcast_id>.json')
def work(podcast_id):

    carousel_images = db.session.query(Event.url).filter(Event.podcast_id==podcast_id).all()
   
    images = {"urls": carousel_images }
    print images

    return jsonify(images)


@app.route('/<int:podcast_id>')
def podcast(podcast_id):
    """Show podcast user has selected"""

    events = Event.query.filter(Event.podcast_id==podcast_id)
    podcast = Podcast.query.get(podcast_id)
    carousel_images = db.session.query(Event.url).filter(Event.podcast_id==podcast_id).all()
    
    images = {podcast_id: carousel_images }

    images = jsonify(images)

    return render_template("podcast.html", events=events, podcast=podcast, images=images)

@app.route('/planet_money')
def planet_money():
    """ API call to NPR Planet Money to get 10 most recent episodes """
    url = 'http://api.npr.org/query?apiKey=MDIwOTI5MjIyMDE0NDUzODQ0NzA3MTJmMw000&numResults=10&format=json&id=94427042&requiredAssets=audio&requiredAssets=text&requiredAssets=image' 

    r = requests.get(url)
    jdict = r.json()

    # Parse a story
    for story in jdict['list']['story']:
        title = story['title']['$text']

        description = story['teaser']['$text']


        if 'show' in story:
            show = story['show'][0]['program']['$text']
        
        image = story['image'][0]['src']
        
        image_caption = ''
        if 'caption' in story:
            image_caption = story['image'][0]['caption']['$text']
        
        audio = story['audio'][0]['format']['mp3'][0]['$text']

        # Add to db...
        new_podcast = Podcast(title, show, description, audio, image, image_caption) 
        
        db.session.add(new_podcast)
        db.session.commit()


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()