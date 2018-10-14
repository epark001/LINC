from flask import Flask, request, abort
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import json
import requests
import os
import MySQLdb

CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
clincHost = os.environ.get('CLINC_HOST')
clincVer = os.environ.get('CLINC_VER')
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')


app = Flask(__name__)

@app.route('/connectSQL', methods=['GET'])
def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)
    return db

@app.route('/fetchSQLvars', methods=['GET'])
def fetchSQLvars(self):
    #"""Simple request handler that shows all of the MySQL variables."""
    self.response.headers['Content-Type'] = 'text/plain'

    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute('SHOW VARIABLES')

    for r in cursor.fetchall():
        self.response.write('{}\n'.format(r))

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
    response = output['visuals']['speakableResponse']
    return reponse

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

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        client = Client(account_sid, auth_token)
        message_history = client.messages.list()
        for message in client.messages.list():
            print (message.body);
            print (message.from_);
            break
        message = client.messages \
            .create(
                body="Hi! Message received",
                from_='+19525294321',
                to='+13476269937'
                )
        return '', 200
    else:
        abort(400)

@app.route("/calls", methods=['GET', 'POST'])
def record():
    """Returns TwiML which prompts the caller to record a message"""
    # Start our TwiML response
    response = VoiceResponse()
    # Use <Say> to give the caller some instructions
    response.say('Hello. Please leave a message after the beep.')
    # Use <Record> to record the caller's message
    response.record()
    # End the call with <Hangup>
    response.hangup()
    return str(response)


if __name__ == '__main__':
    app.run()
