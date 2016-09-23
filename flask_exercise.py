from flask import Flask, request

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

if __name__ == '__main__':
    app.run()
