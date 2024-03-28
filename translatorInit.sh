#! /bin/bash
echo 'Updating packages'
sudo apt update
echo 'Packages updated successfully'
echo ''
echo 'Installing pip'
sudo apt install pip
echo 'pip installed successfully'
echo ''
echo 'Installing gtts'
pip install gtts
echo 'gtts installed successfully'
echo ''
echo 'Installing googletrans'
pip install googletrans==3.1.0a0
echo 'googletrans installed successfully'
echo ''
echo 'Installing pygame'
pip install pygame
echo 'pygame installed successfully'

