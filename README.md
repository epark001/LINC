## Inspiration
This project is inspired by National Coming Out Day which was observed this past week. National Coming Out Day is an annual LGBT awareness day recognizing the challenges that lesbian, gay, bisexual, and transsexual people face in today's society. We wanted to created an easy to use chat AI which can provide an avenue of support for those unable or hesitant to seek help from real people.

## How I built it
For this project, we integrated the Clinc, Twilio, and Google Cloud Platform APIs. LINC's model is built and trained using Clinc's conversational AI platform. We created a python flask server to send queries to the model and parse the responses we get from it. We deployed the server using Google App Engine. Using Twilio's messaging APIs, we made LINC accessible through SMS text messaging as well as through voiced phone calls with text to speech.

## Challenges I ran into
Throughout the course of the hackathon, we ran into challenges in both creating our conversational AI along with creating the server to externally get and send queries. Challenges within Clinc ranged from designing our state graph fluidly to passing variables between competencies. Other challenges included deploying the server as a real world application and the unpredictability of the combination of our APIs. 

## Accomplishments that I'm proud of
Building a versatile chat application using our own server and AI model.

## What's next for LINC
An improved AI model to work with a wider range of support conversations an LGBT person might have and more functionalities within our application itself.
