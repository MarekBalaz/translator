#from gtts import gTTS
#from googletrans import Translator
#from io import BytesIO
#from pygame import mixer
#import time

#print('translating')

#text = 'Marek is a good person'
#translator = Translator(service_urls=['translate.googleapis.com'])
#translation = translator.translate(text, dest='sk', src='en')

#print('running speech')

#mp3_fp = BytesIO()
#tts = gTTS(text=translation.text, lang='sk', slow=False)
#tts.write_to_fp(mp3_fp)
#mixer.init()
#mp3_fp.seek(0)
#mixer.music.load(mp3_fp)
#mixer.music.play()
#time.sleep(3)
#mixer.music.stop()

import urllib.request
urllib.request.urlretrieve('https://argosopentech.nyc3.digitaloceanspaces.com/argospm/translate-es_en-1_0.argosmodel', 'translate-ru_en-1_0.argosmodel')

from argostranslate import package
package.install_from_path('translate-es_en-1_0.argosmodel')