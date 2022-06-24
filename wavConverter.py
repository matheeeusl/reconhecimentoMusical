import os
from pydub import AudioSegment

DATASET_PATH = "./"


for dirpath, dirnames, filenames in os.walk(DATASET_PATH):
  if dirpath is not DATASET_PATH:
    for filename in filenames:
      extension = os.path.splitext(filename)[1]
      if "mp3" in extension:
        src = dirpath +'/' + filename
        dst = dirpath + '/Wav/' + os.path.splitext(filename)[0] + '.wav'
        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav");