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
def root_route():
    return redirect('/podcasts')

@app.route('/podcasts')
def podcasts_index():
    """ Homepage """
    podcasts = Podcast.query.order_by(Podcast.podcast_id.desc())
    user_id = session.get('user_id')
    user = db.session.query(User.name, User.profile_image, User.facebook).filter(User.user_id==user_id).first()

    return render_template("podcasts/index.html", podcasts=podcasts, user=user)

@app.route('/login')
def login():
    """ Login """
    return render_template('login.html')

@app.route('/logout')
def logout():
    """ Logout """
    session.clear()
    return render_template('logout.html')

@app.route('/login-fb', methods=['POST'])
def login_fb():
    user_name = request.form['user_name']
    facebook = request.form['facebook_id']

    user = db.session.query(User.user_id).filter(User.facebook==facebook).first()
    image = None

    if user == None:
        user = User(image, user_name, facebook)
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user.user_id
    return jsonify("")

@app.route('/images/<int:podcast_id>.json')
def show_image_json(podcast_id):
    """ Show carousel images """
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

@app.route('/podcasts/<int:podcast_id>')
def show_podcast(podcast_id):
    """ Show podcast user has selected """
    podcast = Podcast.query.get(podcast_id)
    comments = Comment.query.filter(Comment.podcast_id==podcast_id).order_by(Comment.comment_id.desc())

    user_id = session.get('user_id')
    user = db.session.query(User.name, User.profile_image).filter(User.user_id==user_id).first()

    return render_template("podcasts/show.html", comments=comments, podcast=podcast, user=user, user_id=user_id)

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

        new_podcast = Podcast(title, show, description, audio, image, image_caption) 

        db.session.add(new_podcast)
        db.session.commit()

        print "Success!"

@app.route('/podcasts/<int:podcast_id>/comments', methods=['POST'])
def add_comment(podcast_id):
    """ Add comment to db """
    comment =  request.form['text']

    user_id = session.get('user_id')
    user = db.session.query(User.name, User.profile_image).filter(User.user_id==user_id).first()
    
    new_comment = Comment(comment, podcast_id, user_id)
    
    db.session.add(new_comment)
    db.session.commit()

    return redirect('/podcasts/' + str(podcast_id) + '/comments')

@app.route('/podcasts/<int:podcast_id>/comments')
def comments_index(podcast_id):
    comments = Comment.query.filter(Comment.podcast_id==podcast_id)
    comment_data = []

    for comment in comments:
        author = comment.user.name
        text = comment.comment
        key = comment.comment_id
        data = { 'key': key, 'author': author, 'text': text}
        comment_data.append(data)

    return jsonify(data=comment_data)

@app.route('/profile')
def profile():
    """ Show user profile """ 
    user_id = session.get('user_id')
    user = db.session.query(User.name, User.profile_image).filter(User.user_id==user_id).first()  

    return render_template("profile.html", user=user)

@app.route('/podcasts/new')
def new_podcast():
    """ Show user podcast upload form """ 
    user_id = session.get('user_id')
    user = db.session.query(User.name, User.profile_image).filter(User.user_id==user_id).first()   

    return render_template("podcasts/new.html", user=user)

@app.route('/podcasts', methods=['POST'])
def create_podcast():
    """ Create podcast """
    title = request.form['title']
    show = request.form['show']
    description = request.form['description']
    audio = request.form['audio']
    image = request.form['image']
    caption = request.form['caption']

    attrs = {}

    for key in request.form:
        values = key.split('_')
        if values[0] == 'resource':
            if values[1] not in attrs:
                attrs[values[1]] = {}
            
            attrs[values[1]][values[2]] = request.form[key]

    new_podcast = Podcast(title, show, description, audio, image, caption)

    db.session.add(new_podcast)
    db.session.commit()
    id = str(new_podcast.podcast_id)

    for index in attrs:
        start = attrs[index]['start']
        end = attrs[index]['end']
        image = attrs[index]['image']
        external_url = attrs[index]['external-url']
        new_resource = Event(start, end, image, external_url, new_podcast.podcast_id)
        db.session.add(new_resource)
        db.session.commit()

    return redirect("/podcasts/" + id)

@app.route('/podcasts/<int:podcast_id>/resources', methods=['POST'])
def save_podcast(podcast_id):
    """ Add resource to db """
    image = request.form['image']
    external_resource = request.form['external-url']
    start = request.form['start']
    end = request.form['end']

    new_resource = Event(start, end, image, external_resource, podcast_id)

    db.session.add(new_resource)
    db.session.commit()

    return redirect('/podcasts/' + podcast_id)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
