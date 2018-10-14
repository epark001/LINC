from flask import Flask, request, abort
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

account_sid = 'ACce3d35b11990b0a5f86d17795ae7ffe6'
auth_token = '33808ddf18ac53ba89ffff98fbf2c460'


app = Flask(__name__)


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
    
