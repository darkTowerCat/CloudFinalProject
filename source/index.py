from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(title=t, author=a, date=d, prep_time=p, ingredients=i) for t, a, d, p, i in model.select()]
        return render_template('index.html',entries=entries)


    def synthesize_text(text):
        """Synthesizes speech from the input string of text."""
        from google.cloud import texttospeech
        client = texttospeech.TextToSpeechClient()

        input_text = texttospeech.types.SynthesisInput(text=text)

        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        response = client.synthesize_speech(input_text, voice, audio_config)

        # The response's audio_content is binary.
        with open('output.mp3', 'wb') as out:
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')
