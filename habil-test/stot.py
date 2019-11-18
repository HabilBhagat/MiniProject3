import speech_recognition as sr
from os import path
import os 

file_name = "sound.wav"
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), file_name)

r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)

try:
    file = open("recognized.txt","w+")
    recog = r.recognize_google(audio)
    print(recog)
    file.write(recog + ". ")
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

os.system("python test3.py")