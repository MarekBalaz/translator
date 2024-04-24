import pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import wave
import RPi.GPIO as GPIO
from transformers import MarianMTModel, MarianTokenizer

GPIO.setmode(GPIO.BCM)
#Gpio pin for switch to turn off and on program
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Gpio pin for translator to start listening
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Gpio pin for Green LED
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Gpio pin for Red LED
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:

    GPIO.output(24, GPIO.HIGH)

    GPIO.wait_for_edge(17, GPIO.RISING)

    stt_model_path = r"/home/marek/vosk-model-small-en-us-0.15"
    model = Model(stt_model_path)
    recognizer = KaldiRecognizer(model, 48000)    

    from_code = "en"
    to_code = "es"

    translator_model_path = r"/home/marek/opus-mt-en-es"
    tokenizer = MarianTokenizer.from_pretrained(translator_model_path)
    model = MarianMTModel.from_pretrained(translator_model_path)

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
        if GPIO.input(17) == GPIO.LOW:
            GPIO.output(23, GPIO.LOW)
            GPIO.output(24, GPIO.HIGH)
            break
        GPIO.wait_for_edge(22, GPIO.RISING)
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

        input_ids = tokenizer.encode(result, return_tensors="pt")

        translated_ids = model.generate(input_ids)

        translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

        print(translated_text)
        print('running speech')
        engine = pyttsx3.init()
        engine.say(translated_text)
        engine.runAndWait()


    
