import os
import flask
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flask.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = flask.app.test_client()
        flask.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flask.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data


if __name__ == '__main__':
    unittest.main()