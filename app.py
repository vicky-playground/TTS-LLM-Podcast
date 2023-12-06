from flask import Flask, render_template, send_file
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Initialize IBM Watson TTS
authenticator = IAMAuthenticator(os.getenv("IBM_WATSON_API_KEY"))
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(os.getenv("IBM_TTS_URL"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['GET'])
def play_audio():
    with open('text_data.json', 'r') as file:
        data = json.load(file)
        text = data['text']

    # Generate the audio in a browser-compatible format, e.g., OGG or MP3 if supported
    response = tts.synthesize(text, voice='en-US_AllisonV3Voice', accept='audio/ogg').get_result()
    audio_file_path = 'output.ogg'
    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(response.content)

    return send_file(audio_file_path, mimetype='audio/ogg', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
