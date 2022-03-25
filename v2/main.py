from configparser import ConfigParser
import json
import os

from pydub import AudioSegment
from pydub.silence import split_on_silence as sos
from pydub.utils import make_chunks as mc
import speech_recognition as sr

def transcribe(file):
  result = ""

  os.chdir(TEMP)
  try:
    os.mkdir(f'{file}_storage')
  except(FileExistsError):
    pass
  os.chdir(f'{file}_storage')

  os.system(f'ffmpeg -i "{os.path.join(PATH, file)}" "{file}.wav"')

  AudioIn = AudioSegment.from_wav(f'{file}.wav')

  text = open(f'{file}_result.txt', 'w+')

  r = sr.Recognizer()

  chunks = sos(AudioIn, min_silence_len = 200, silence_thresh = -42)

  try:
    os.mkdir('audio_chunks')
  except(FileExistsError):
    pass

  os.chdir("audio_chunks")

  i=0

  for chunk in chunks:
    print(f"saving chunk{i}.wav")
    chunk.export(f"./chunk{i}.wav", bitrate="192k", format="wav")

    filename = f"chunk{i}.wav"

    print(f"processing chunk {i}")
    file = filename

    with sr.AudioFile(file) as source:
      audio = r.listen(source)

    try:
      rec = r.recognize_google(audio)
      text.write(rec+". ")
      result+=(f'{rec}. ')
    except sr.UnknownValueError:
      print("Could not understand audio")
    except sr.RequestError as e:
      print("Could not request results. check your internet connection")

    i += 1

  os.chdir(TEMP)
  os.rmdir(f'{file}_storage')
  return result

if __name__ == "__main__":
  config = ConfigParser()

  config.read('v2/config.ini')

  PATH = config.get('directory', 'storage')
  os.chdir(PATH)

  try:
    os.mkdir(f'temp')
  except(FileExistsError):
    pass
  TEMP = os.path.join(PATH, 'temp')
  result = []

  for file in os.listdir(PATH):
      if file.endswith(('.mp4', '.mp3', '.wav')):

        print(os.path.join(PATH, file) + ' detected. Transcribing')
        text = transcribe(file)

        item = {'name' : file}
        item['text'] = text
        
        result.append(item)
  
  jsonData = json.dumps(result, indent = 2)

  with open("out.json", "w") as outfile:
    outfile.write(jsonData)

  print('fin')