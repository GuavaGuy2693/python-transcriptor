from configparser import ConfigParser
import os

import __brain

transcribe = __brain.transcribe

if __name__ == "__main__":
  config = ConfigParser()

  config.read('config.ini')

  PATH = config.get('directory', 'storage')
  os.chdir(PATH)

  
  result = []

  for file in os.listdir(PATH):
      if file.endswith(('.mp4', '.mp3', '.wav')):

        print(os.path.join(PATH, file) + ' detected. Transcribing')
        text = transcribe(file, PATH)

  print('fin')