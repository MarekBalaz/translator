import pyttsx3
import sys
import json
import os
from vosk import Model, KaldiRecognizer
import pyaudio
import wave
import RPi.GPIO as GPIO
import time
import argostranslate.package
import argostranslate.translate

GPIO.setmode(GPIO.BCM)
#Gpio pin for switch to turn off and on program
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Gpio pin for translator to start listening
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Gpio pin for Green LED
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Gpio pin for Red LED
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def cleanup_callback():
    GPIO.cleanup()

GPIO.add_event_detect(17, GPIO.FALLING, callback=cleanup_callback)


GPIO.output(24, GPIO.HIGH)

GPIO.wait_for_edge(17, GPIO.RISING)
isStarted = GPIO.input(17)
if isStarted == True:
    model = Model(r"/home/marek/Desktop/vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 48000)    

    from_code = "en"
    to_code = "es"
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "translation.wav"

    p = pyaudio.PyAudio()
    GPIO.output(24, GPIO.LOW)
    GPIO.output(23, GPIO.HIGH)
    
    while True:
        GPIO.wait_for_edge(27, GPIO.RISING)
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


        # Sample audio file for recognition
        audio_file = WAVE_OUTPUT_FILENAME

        # Open the audio file
        with open(audio_file, "rb") as audio:
            while True:
                # Read a chunk of the audio file
                data = audio.read(4000)
                if len(data) == 0:
                    break
                # Recognize the speech in the chunk
                recognizer.AcceptWaveform(data)

        # Get the final recognized result
        result = recognizer.FinalResult()
        print(result)

        print('translating')

        translatedText = argostranslate.translate.translate(result, from_code, to_code)

        print(translatedText)
        print('running speech')
        engine = pyttsx3.init()
        engine.say(result)
        engine.runAndWait()
else:
    for i in range(0, 5):
        GPIO.output(24, GPIO.LOW)
        time.sleep(0.7)
        GPIO.output(24, GPIO.HIGH)
    GPIO.cleanup()


    
