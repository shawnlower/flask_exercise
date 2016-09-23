#!/usr/bin/python

import unittest

from flask import json

from flask_exercise import app

import os

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

    def test_accept_json(self):
        """
        Test that we get a proper response when we set the Accept header
        to 'application/json'
        """
        expected_output = '{"message": "Good morning"}'

        response = self.app.get('/', headers = {'Accept': 'application/json'})
        self.assertEqual(response.data, expected_output)

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client(self)
        self.app.application.config['SERVER_MODE'] = True

    def test_post_in_server_mode(self):
        """
        When run in server mode (specified by setting the environment variable
        SERVER_MODE to a truthy value (i.e. the strings 1 or true), the server
        will expect a JSON dictionary to be in our POST data, with a key of
        'foo', and will return the key's value in the POST response.
        This value must also be emitted into the server logs.
        """
        post_data = {"foo": "The foo from the unittest!"}
        expected_output = post_data['foo']

        response = self.app.post('/', data=json.dumps(post_data))
        self.assertEqual(response.data, expected_output)

class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client(self)
        self.app.application.config['SERVER_MODE'] = False

    def test_post_in_client_mode(self):
        """
        When run in client mode (specified by setting the environment variable
        SERVER_MODE to a falsey value (i.e. the strings 0 or false), the server
        will expect a JSON dictionary to be in our POST data, with a key of
        'bar', and will return the key's value in the POST response.
        This value must also be emitted into the server logs.
        """
        post_data = {"bar": "The bar from the unittest!"}
        expected_output = post_data['bar']

        response = self.app.post('/', data=json.dumps(post_data))
        self.assertEqual(response.data, expected_output)


if __name__ == '__main__':
    unittest.main()

