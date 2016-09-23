import unittest

from flask import json

from flask_exercise import app

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client(self)

    def test_index(self):
        """Send a basic request"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_accept_text(self):
        """Test that we get a proper response when we set the Accept header
           to 'text/html'"""
        expected_output = "<p>Hello, World</p>"

        response = self.app.get('/', headers = {'Accept': 'text/html'})
        self.assertEqual(response.data, expected_output)

