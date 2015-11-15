"""Podcast Storybook."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, json, jsonify
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from json import dumps
from model import Podcast, Event, User, Comment, connect_to_db, db
import requests
import os

# Import NPR API KEY
npr_auth_token = os.environ['NPR_AUTH_TOKEN']

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Prevent jinja from failing silently
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    podcasts = Podcast.query.all()
    #Only selects first user. 
    user = User.query.first()


    return render_template("index.html", podcasts=podcasts, user=user)


@app.route('/images/<int:podcast_id>.json')
def work(podcast_id):
    """Show carousel images"""
    image_data = db.session.query(Event.image_url, Event.start_at, Event.end_at, Event.link).filter(Event.podcast_id==podcast_id).all()
    images = []
    podcast = Podcast.query.get(podcast_id)
    title_image = podcast.image
    title_attrs = { "image_url": title_image, "start_at": 0, "end_at": 0, "link": None }
    images.append(title_attrs)

    for data in image_data:
        image_attrs = { "image_url": data[0], "start_at": data[1], "end_at": data[2], "link": data[3] }
        images.append(image_attrs)

    result = { "data": images }

    return jsonify(result)



@app.route('/<int:podcast_id>')
def podcast(podcast_id):
    """Show podcast user has selected"""
    # TODO I don't think this events query is being used for anything...
    events = Event.query.filter(Event.podcast_id==podcast_id)
    podcast = Podcast.query.get(podcast_id)
    comments = Comment.query.filter(Comment.podcast_id==podcast_id)

    #Only selects first user. 
    user = User.query.first()
    user_id = user.user_id

    return render_template("podcast.html", events=events, comments=comments, podcast=podcast, user=user, user_id=user_id)

@app.route('/planet_money')
def planet_money():
    """ API call to NPR Planet Money to get 10 most recent episodes """
    
    url = 'http://api.npr.org/query?apiKey=' + npr_auth_token + '&numResults=10&format=json&id=94427042&requiredAssets=audio&requiredAssets=text&requiredAssets=image' 

    r = requests.get(url)
    jdict = r.json()

    # Parse a story returned from query
    for story in jdict['list']['story']:
        title = story['title']['$text']

        description = story['teaser']['$text']

        show = None
        if 'show' in story:
            show = story['show'][0]['program']['$text']
        
        image = story['image'][0]['src']
        
        image_caption = None
        if 'caption' in story:
            image_caption = story['image'][0]['caption']['$text']
        
        audio = story['audio'][0]['format']['mp3'][0]['$text']

        # Add podcast to db...
        new_podcast = Podcast(title, show, description, audio, image, image_caption) 

        db.session.add(new_podcast)
        db.session.commit()

        print "Success!"

@app.route('/addComment', methods=['POST'])
def add_comment():
    """Add comment to db"""

    comment =  request.form['comment']
    podcast_id = 3
    user_id = 1
    user = User.query.get(user_id)
    profile_image = user.profile_image
    user_name = user.first_name + ' ' + user.last_name
    # Add comment to db
    new_comment = Comment(comment, podcast_id, user_id)

    
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(comment=comment, profile_image=profile_image, user_name=user_name)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()