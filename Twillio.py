from functools import wraps

from twilio.twiml.voice_response import VoiceResponse,Gather, VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator


from flask import (
    Flask,
    abort,
    current_app,
    request,
)

import os


app = Flask(__name__)


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN'))

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid or current_app.debug:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function


@app.route('/voice', methods=['POST'])
@validate_twilio_request
def incoming_call():
    """Twilio Voice URL - receives incoming calls from Twilio"""
    # Create a new TwiML response

    resp = VoiceResponse()
    resp.gather()
    print(resp)
    response.pause(length=3)

    # <Say> a message to the caller
    from_number = request.form['From']
    body = """
    Thanks for calling!
    Your phone number is {0}. I got your call because of Twilio's webhook.
    Goodbye!""".format(' '.join(from_number))
    resp.say(body)

    # Return the TwiML
    return str(resp)


@app.route('/message', methods=['GET', 'POST'])
@validate_twilio_request
def incoming_message():
    #"""Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()
    # Add a message
    resp.message("The Robots are coming! Head for the hills!")
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
