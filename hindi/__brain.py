#imports
import os

from pydub import AudioSegment, effects
from pydub.silence import split_on_silence as sos
from pydub.utils import make_chunks as mc
import speech_recognition as sr

#audio normalization
def normalize_audio(sound, target_dDFS):
  change_in_dBFS = target_dDFS - sound.dBFS
  return sound.apply_gain(change_in_dBFS)

#audio transcription
def transcribe(file, PATH):
  result = ""

#creating temp dirs
  try:
    os.mkdir(f'temp')
  except(FileExistsError):
    pass
  TEMP = os.path.join(PATH, 'temp')

  os.chdir(TEMP)
  try:
    os.mkdir(f'{file}_storage')
  except(FileExistsError):
    pass
  os.chdir(f'{file}_storage')

#converting to .wav file
  os.system(f'ffmpeg -i "{os.path.join(PATH, file)}" "{file}.wav"')

#Speech recognition
  AudioIn = AudioSegment.from_wav(f'{file}.wav')
  AudioIn = normalize_audio(AudioIn, -20)

  text = open(f'{os.path.join(PATH, f"{file}_result.txt")}', 'w+', encoding='utf-8')
  
  #initialization
  r = sr.Recognizer()
  
  #spliting into chunks
  chunks = sos(AudioIn, min_silence_len = 200, silence_thresh = -40)

  try:
    os.mkdir('audio_chunks')
  except(FileExistsError):
    pass

  os.chdir("audio_chunks")

  i=0

  #processing chunks
  for chunk in chunks:
    print(f"saving chunk{i}.wav")
    chunk.export(f"./chunk{i}.wav", bitrate="192k", format="wav")

    filename = f"chunk{i}.wav"

    print(f"processing chunk {i}")
    file = filename

    with sr.AudioFile(file) as source:
      audio = r.listen(source)

    try:
      rec = r.recognize_google(audio, language='hi-In')
      text.write(rec+". ")
      result+=(f'{rec}. ')
    except sr.UnknownValueError:
      print("Could not understand audio")
    except sr.RequestError as e:
      print("Could not request results. check your internet connection")

    i += 1
  
  #end
  text.close()
  os.chdir(TEMP)