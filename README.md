## Welcome to Story Strata

Every story has many layers, Story Strata is intended for podcast enthusiasts that want to dig deeper. 
The creation of a podcast requires a massive amount of research.  Some of these valuable details may be left on the cutting floor during the editing process due to being too tangential to the story or unsuited to the audio medium. The app enhances the podcast experience by giving users access to extra related content in an unobtrusive format.
With Story Strata users can listen like they normally would, but with the option to explore the story further. As the audio plays, users have the option of engaging with live updating images, websites and other resources, as well as to discuss episodes with other users through comments.

## Getting Started

1. Install Requirements at the command prompt if you haven't yet:

        $ pip install requirements.txt

2. Create the database:

        $ python -i model.py
        > db.create_all()

3. Seed the database:

        $ python seed.py

4. Start the server:
        
        $ python server.py

5. Go to a web browser and visit http://localhost:5000
