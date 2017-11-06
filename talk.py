from gtts import gTTS
import os

def speak(text):
    file = "voice.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(file)
    os.system("mpg321 " + file)
    os.remove(file)

