
#pip install SpeechRecognition

#initiliasing recogniser
import speech_recognition as sr 
r = sr.Recognizer()  
#recording audio from wav file
with sr.WavFile("test.wav") as source:
	audio = r.record(source)
#attempting detection
try:
	print(r.recognize(audio))
except LookupError:
	print("Could not understand audio")