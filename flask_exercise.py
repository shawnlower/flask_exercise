from flask import Flask, request
import json
import logging
import os

app = Flask(__name__)

@app.route('/')
def main():
    # Inspect the list of the accepted types returned by the client, as per RFC2616.
    accept = request.headers.get('Accept', "").split(',')

    # Return our hello message as either text or json, depending on the value
    # NOTE: it's possible for the client to pass both values, in which case we
    # default to the first case
    if 'text/html' in accept:
        return "<p>Hello, World</p>"
    elif 'application/json' in accept:
        return '{"message": "Good morning"}'
    else:
        # Some clients, e.g. curl, set Accept to '*/*'
        return 'This behavior is undefined by the homework assignment, but I\'m going to say hello anyhow.\n'

@app.route('/', methods=['POST'])
def post_index():
    # Method that receives data POST-ed to the '/' resource
    # Our application can run in either of two ways, as specified by the
    # SERVER_MODE environment variable.
    #    'true', or '1': we will expect to receive a JSON dictionary with a key 'foo'
    #         and will return the value for the key in our response.
    #    'false', of '0': we will expect to receive a JSON dictionary with a key 'bar'
    #         and will return the value for the key in our response.
    # If neither of these cases match, we will return an error

    # Determine whether we're in server mode
    if app.config['SERVER_MODE']:
        key = 'foo'
    else:
        key = 'bar'

    try:
        data = json.loads(request.data)
    except ValueError:
        # Unparseable JSON data, return a 400 Bad Request
        return "Bad Request (Invalid JSON payload)", 400

    if not key in data:
        # Neither 'foo', nor 'bar' found in JSON data
        return "Bad Request (Key not found in JSON)", 422


    # Write to the logs
    app.logger.info("Someone posted a {} containing '{}'".format(key, data[key]))

    # Write out our response
    return data[key]

        # self.app.logger.error

@app.before_first_request
def setup():
    # Setup our application, including configuration settings

    # Determine whether we should be in server mode.
    server_mode = os.environ.get('SERVER_MODE', 'true')
    if server_mode.lower() == 'true' or server_mode == '1':
        app.config['SERVER_MODE'] = True
    elif server_mode.lower() == 'false' or server_mode == '0':
        app.config['SERVER_MODE'] = False
    else:
        raise Exception('Invalid SERVER_MODE setting. Expected "true" or "false"')

    # Setup logging
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

    app.logger.info("Server mode set to {}".format(str(app.config['SERVER_MODE'])))

if __name__ == '__main__':
    setup()
    app.run()
