from flask import Flask, request, abort
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import json
import requests
import os
#import datetime
import logging
import unicodedata


from bson import json_util
from datetime import datetime, timedelta, timezone
#import unix_socket
#from flask_sqlalchemy import SQLAlchemy
#import sqlalchemy
#import MySQLdb

latest_transcript =""


CLOUDSQL_CONNECTION_NAME = os.environ.get("CLOUDSQL_CONNECTION_NAME")
CLOUDSQL_USER = os.environ.get("CLOUDSQL_USER")
CLOUDSQL_PASSWORD = os.environ.get("CLOUDSQL_PASSWORD")
clincHost = os.environ.get("CLINC_HOST")
clincVer = os.environ.get("CLINC_VER")
#account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
account_sid = "ACce3d35b11990b0a5f86d17795ae7ffe6"
#auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
auth_token = "33808ddf18ac53ba89ffff98fbf2c460"

#app1.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
#app1.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db = SQLAlchemy(app1)


app = Flask(__name__)



@app.route("/calls", methods=['GET', 'POST'])
def record():
    unicodedata.normalize('NFKD', latest_transcript).encode('ascii','ignore')
    while (latest_trancript != "Goodbye"):
        client = Client(account_sid, auth_token)
        # Start our TwiML response
        response = VoiceResponse()
        response.say('Please say goodbye')
        response.record(transcribe=True, playBeep=True,timeout=4)
        # Use <Say> to give the caller some instructions
        response.say('Hello this is reponse. What would you like to talk about?')
        # Use <Record> to record the caller's message
        response.record(transcribe=True, playBeep=True,timeout=4)
        # response.pause(length=3)
        client = Client(account_sid, auth_token)
        trans_list = client.transcriptions.list()
        for transcription in trans_list:
            latest_transcript = transcription.transcription_text
            status= transcription.status
    response.say('Please say goodbye')
    response.hangup();
    return str(response)

def queryClinc(inputQuery, phoneNum):
    #url = "https://"+hostname+"/"+version+"/query"
    url = "https://mhacks.clinc.ai/v1/query"
    headers = {
        "Authorization": authClinc(),
        "Content-Type":"application/json"
    }
    payload = {
        "query": inputQuery,
        "lat": 42.2730207,
        "lon": -83.7517747,
        "time_offset": 300,
        "device": "Mozilla/5.0"
    }
    text_file = open("sessionLogs.txt","r")
    logs = json.loads(text_file.read(), object_hook=json_util.object_hook)
    text_file.close()
    if phoneNum in logs:
        if logs[phoneNum]["lastSeen"]+timedelta(hours=1) > datetime.now(tz=timezone.utc):
            payload["dialog"] = logs[phoneNum]["dialog"]
    else:
        logs[phoneNum] = {}
    output = requests.post(url, data = json.dumps(payload), headers = headers)
    output = json.loads(output.text)
    #print(output["dialog"])
    # logs[phoneNum] = {
    #     "dialogue": output["dialogue"],
    #     "lastSeen": timedelta.now()
    # }
    logs[phoneNum]["dialog"] = output["dialog"]
    logs[phoneNum]["lastSeen"] = datetime.now(tz=timezone.utc)

    print(logs)

    raw = open("sessionLogs.txt", "w")
    # contents = json.loads(raw.read())
    # raw.seek(0)
    # raw.truncate()
    raw.write(json.dumps(logs, default=json_util.default))
    raw.close()

    return output["visuals"]["speakableResponse"]

def authClinc():
    authForm = {
        "client_id":"clinc",
        "client_secret":"clinc",
        "username":"edward",
        "password":"12345678",
        "grant_type":"password",
        "institution":"mhacks2"
    }
    url = "https://mhacks.clinc.ai/v1/oauth"

    #url = "https://"+hostname+"/"+version+"/oauth"
    output = requests.post(url, data = authForm )
    output = json.loads(output.text)
    return "Bearer "+output["access_token"]

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        client = Client(account_sid, auth_token)
        message_history = client.messages.list()
        for message in client.messages.list():
            #print(message.body);
            textBody = message.body;
            #print(message.from_);
            phoneNum = message.from_;
            break

        output = queryClinc(textBody, phoneNum)

        message = client.messages \
            .create(
                body=output,
                from_="+19525294321",
                to=phoneNum
                )
        return "", 200
    else:
        abort(400)

@app.errorhandler(500)
def server_error(e):
    logging.exception("An error occurred during a request.")
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == "__main__":
    app.run()
