# Python Transcriptor
## Video speech text extractor
This python program takes video input and generates text output containing detected speech.
Currently supported languages:
  - English
  - Hindi
## Prerequisites:
  - python 3.x
  - ffmpeg
## Python dependencies
  - os
  - SpeechRecognition
  - pydub
## To process video
  - Add videos to Storage folder
  - For language character output, open its folder in a terminal (English/Hindi)
  - run command
  ```
  python main.py
  ```
  - Output will be generated in the storage folder with name `{file}_result.txt`
