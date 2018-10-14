from functools import wraps

from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
import json
import requests

from flask import (
    Flask,
    abort,
    current_app,
    request,
)

import os

clincHost = "mhacks.clinc.ai"
clincVer = "v1"

app = Flask(__name__)

@app.route('/query', methods=['POST']) 
def queryPost():
    print("hullo")
    return "henlo"

def queryClinc(inputQuery):
    headers = {
        "Authorization": authClinc(),
        "Content-Type":"application/json"
    }
    payload = {
        'query': inputQuery,
        'lat': 42.2730207,
        'lon': -83.7517747,
        'time_offset': 300,
        'device': 'Mozilla/5.0'
    }
    url = "https://"+hostname+"/"+version+"/query"
    output = requests.post(url2, data = json.dumps(payload), headers = headers)
    output = json.loads(output.text)
    output['visuals']['speakableResponse']


def authClinc():
    authForm = {
        "client_id":"clinc",
        "client_secret":"clinc",
        "username":"edward",
        "password":"12345678",
        "grant_type":"password",
        "institution":"mhacks2"
    }

    url = "https://"+hostname+"/"+version+"/oauth"
    output = requests.post(url, data = form )
    output = json.loads(output.text)
    return "Bearer "+output['access_token']


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

    # <Say> a message to the caller
    from_number = request.form['From']
    body = """
    Thanks for calling!
    Your phone number is {0}. I got your call because of Twilio's webhook.
    Goodbye!""".format(' '.join(from_number))
    resp.say(body)

    # Return the TwiML
    return str(resp)


@app.route('/message', methods=['POST'])
@validate_twilio_request
def incoming_message():
    """Twilio Messaging URL - receives incoming messages from Twilio"""
    # Create a new TwiML response
    resp = MessagingResponse()

    # <Message> a text back to the person who texted us
    body = "Your text to me was {0} characters long. Webhooks are neat :)" \
        .format(len(request.values['Body']))
    resp.message(body)

    # Return the TwiML
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
