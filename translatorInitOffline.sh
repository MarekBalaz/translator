#! /bin/bash
sudo apt update -y

sudo apt upgrade -y

sudo apt install python -y

sudo apt install pip -y

sudo apt install git -y

sudo apt install espeak -y

pip install vos

pip install pyttsx3

pip install pydub

pip install pyaudio

pip install torch

pip install sentencepiece

pip install git+https://github.com/huggingface/transformers

pip install huggingface -----------------------------------------> check if this is necessary

cd ~

wget "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
unzip "vosk-model-small-en-us-0.15"

sudo apt install git-lfs -y

git lfs install

git clone https://huggingface.co/Helsinki-NLP/opus-mt-es-en

cd opus-mt-es-en

git lfs pull

cd ~

sudo pip3 install --upgrade adafruit-python-shell

wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py

echo -e "y\ny" | sudo python3 i2smic.py

echo "dtoverlay=hifiberry-dac" >> /boot/config.txt

sudo apt update -y

sudo shutdown -r now