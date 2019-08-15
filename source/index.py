from flask import render_template
from flask.views import MethodView
import gbmodel
import json
import hashlib
from google.cloud import texttospeech
import os.path

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = []
        for t, a, d, p, i in model.select():
            entry = dict(title=t, 
                        author=a, 
                        date=d, 
                        prep_time=p, 
                        ingredients=i,
                        mp3_path = synthesize_text(i)
                    )
            entries.append(entry) 
        return render_template('index.html', entries=entries)


def synthesize_text(text):
    name = hashlib.sha256()
    name.update(text.encode())
    name = name.hexdigest()
    mp3_path = f"./static/{name}.mp3"
    
    if os.path.isfile(mp3_path):
        return mp3_path
    """Synthesizes speech from the input string of text."""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=text)
    # API parameters set
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # Generated mp3 is then saved to external file is static folder 
    with open(mp3_path, 'wb') as out:
        out.write(response.audio_content)
    return mp3_path
