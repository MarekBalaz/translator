#! /bin/bash
echo 'Updating packages'
sudo apt update
echo 'Packages updated successfully'
echo ''
echo 'Upgrading packages'
sudo apt upgrade -y
echo 'Packages upgraded successfully'
echo ''
echo 'Installing pip'
sudo apt install pip
echo 'pip installed successfully'
echo ''
echo 'Installing espeak'
pip install python-espeak -----------------------------> INSTALL
echo 'espeak installed successfully'
echo ''
echo 'Installing vos'
pip install vos
echo 'vos installed successfully'
echo ''
echo 'Installing pyttsx3'
pip install pyttsx3
echo 'pyttsx3 installed successfully'
echo ''
echo 'Installing pydub'
pip install pydub
echo 'pydub installed successfully'
echo ''
echo 'Installing pyaudio'
pip install pyaudio
echo 'pyaudio installed successfully'
wget "vosk-model-small-en-us-0.15"
unzip "vosk-model-small-en-us-0.15"

https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip