import os
import librosa
import math
import json

DATASET_PATH = "./"
JSON_PATH = "data.json"

SAMPLE_RATE = 22050
DURATION = 0.1 #measured in sec.
SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION

def save_mfcc(dataset_path, json_path, n_mfcc= 40, n_fft=2048, hop_length=512, num_segments=5):
  data = {
    "mapping": [],
    "mfcc": [],
    "labels": []
  }
  num_samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
  
  #loop the folders.
  for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):
    
    # ensure that we're not at the root level
    if dirpath is not dataset_path and "MP3" not in dirpath :
      
      #save the semantic label
      dirpath_components = dirpath.split("/")
      semantic_label = dirpath_components[-1]
      data["mapping"].append(semantic_label)
      print("\nProcessing {}".format(semantic_label))
      # process files for a specific genre
      for f in filenames:
        
        # load audio file
        file_path = os.path.join(dirpath, f)
        signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)
        
        #process segments extracting mfcc and storing data
        for s in range(num_segments):
          start_sample = num_samples_per_segment * s # s=0 -> 0
          finish_sample = start_sample + num_samples_per_segment #s=0 -> num_samples_per_segment
          
          mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample], sr=sr, n_fft=n_fft, n_mfcc=n_mfcc,hop_length=hop_length)
          mfcc = mfcc.T

          data["mfcc"].append(mfcc.tolist())
          data["labels"].append(i-1)
          print("{}, segment: {}".format(file_path, s+1))
            
  with open(json_path, "w") as fp:
    json.dump(data, fp, indent=4);
    
if __name__ == "__main__":
  save_mfcc(DATASET_PATH, JSON_PATH, num_segments=10)
            
            