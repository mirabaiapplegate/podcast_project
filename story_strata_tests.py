import os
from server import app
from model import connect_to_db
import unittest
from flask import url_for
import tempfile

class StoryStrataTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        connect_to_db(app)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_podcasts_index(self):
        response = self.app.get('/podcasts')
        assert 'Podcast' in response.data

    def test_form(self):
        response = self.app.get('/podcasts/new')
        assert 'Upload Podcast' in response.data

if __name__ == '__main__':
    unittest.main()