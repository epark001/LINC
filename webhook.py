from flask import Flask, request, abort
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import unicodedata

#real
account_sid = 'ACce3d35b11990b0a5f86d17795ae7ffe6'
auth_token = '33808ddf18ac53ba89ffff98fbf2c460'
##test
#account_sid = 'AC88a96de03a704efb9b406e2fd12594cf'
#auth_token = 'eb8c884d2caafaa6ea643217845a3420'
latest_transcript =""

app = Flask(__name__)


#def clearRecordings():
#    client = Client(account_sid, auth_token)
#    trans_list = client.transcriptions.list()
#    for transcription in trans_list:
#        latest_transcript = transcription.transcription_text


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        client = Client(account_sid, auth_token)
        message_history = client.messages.list()
        #print(client.transcriptions.list())
        trans_list = client.transcriptions.list()
        for transcription in trans_list:
            latest_transcript = transcription.transcription_text
            print(transcription.sid);
            print(latest_transcript);
        print("printed transcript")
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

@app.route("/voice_response", methods = ['GET','POST'])
def voice_response():
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
     
@app.route("/calls", methods=['GET', 'POST'])
def record():
    client = Client(account_sid, auth_token)
    # Start our TwiML response
    response = VoiceResponse()
    # Use <Say> to give the caller some instructions
    response.say('Hello this is LINC. What would you like to talk about?')
    # Use <Record> to record the caller's message
    response.record(transcribe=True, playBeep=True,timeout=4)
    # response.pause(length=3)
    client = Client(account_sid, auth_token)
    trans_list = client.transcriptions.list()
    for transcription in trans_list:
        latest_transcript = transcription.transcription_text
        status= transcription.status
        if(latest_transcript!=None):
            unicodedata.normalize('NFKD', latest_transcript).encode('ascii','ignore')
            print(status);
            print(transcription.sid);
            print(latest_transcript);
            transcription.delete();
            break
        else:
            response.say("I'm sorry. I didn't get that. Can you repeat it?")
    print(latest_transcript != "hello")
    if (latest_transcript != "hello"):
        print("boolean worked");
        response.redirect("http://4b930e15.ngrok.io/voice_response")
    response.hangup()
    return str(response)




if __name__ == '__main__':
    #clearRecordings();
    app.run()
    

