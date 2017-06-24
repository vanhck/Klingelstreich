import json
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1

text_to_speech = TextToSpeechV1(
    username='6332656d-4980-42e6-b4e2-76a60e1a88c2',
    password='DD1VldLTdUFF',
    x_watson_learning_opt_out=True)  # Optional flag

#print(json.dumps(text_to_speech.voices(), indent=2))

with open(join(dirname(__file__), 'resources/output.wav'),
          'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize('Hallo Welt!', accept='audio/wav',
                                  voice="de-DE_BirgitVoice"))

#print(
#    json.dumps(text_to_speech.pronunciation(
#        'Watson', pronunciation_format='spr'), indent=2))

#print(json.dumps(text_to_speech.customizations(), indent=2))
