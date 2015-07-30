#pip install SpeechRecognition
#cd to directory with PyAudio-0.2.8-cp34-none-win32.whl
#pip install PyAudio-0.2.8-cp34-none-win32.whl
import speech_recognition as sr
r = sr.Recognizer("en-GB")
with sr.Microphone() as source:                
    print("Adjusting audio levels")
    r.adjust_for_ambient_noise(source, duration = 3)
    print("Microphone listening")
    audio = r.listen(source)
    print("Finished listening")

try:
    print("You said " + r.recognize(audio))    
except LookupError:                            
    print("Could not understand audio")