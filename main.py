from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import make_chunks
import speech_recognition as sr
import os

PATH = input()

wavCommand = f"ffmpeg -i {PATH} out.wav"

os.system(wavCommand)

audioIn = AudioSegment.from_wav("out.wav")

fh = open("recognized.txt", "w+")

r = sr.Recognizer()

with sr.AudioFile("out.wav") as source:

  audio = r.listen(source)

  try:
    rec = r.recognize_google(audio)
    fh.write(rec+". ")

  except sr.UnknownValueError:
    print("Could not understand audio")
    
  except sr.RequestError as e:
    print("Could not request results. check your internet connection")

# chunks = split_on_silence(audioIn, min_silence_len=200, silence_thresh=-50)

# try:
#   os.mkdir('audio_chunks')
# except(FileExistsError):
#   pass

# os.chdir("audio_chunks")

# i=0

# for chunk in chunks:
#   print(f"saving chunk{i}.wav")
#   chunk.export(f"./chunk{i}.wav", bitrate="192k", format="wav")

#   filename = f"chunk{i}.wav"

#   print(f"processing chunk {i}")
#   file = filename

#   r = sr.Recognizer()

#   with sr.AudioFile(file) as source:
#     audio = r.listen(source)

#   try:
#     rec = r.recognize_google(audio)
#     fh.write(rec+". ")
#   except sr.UnknownValueError:
#     print("Could not understand audio")
#   except sr.RequestError as e:
#     print("Could not request results. check your internet connection")

#   i += 1

# os.chdir("..")