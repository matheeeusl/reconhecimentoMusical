# Método 1:
# Detecta manualmente a afinação da anota, se é um Dó, Ré ou Mi.

#Imports
import parselmouth
import numpy as np
import os

# Variavel Global
AFINACAO_RANGE = 5
# full, short, hard
LOG_TYPE = "short"

DATASET_PATH = "./"

# detect_audio()

# Pega a música:
# snd = parselmouth.Sound("./Escala Cromatica - video youtube/E4.mp3")
#   snd = parselmouth.Sound("./Variações Dó/Dó 4t/J Arban Pag 12 N.7 C3 1.mp3")
# snd = parselmouth.Sound(WAVE_OUTPUT_FILENAME)

# Pega a média de tons dentro da música
def average_pitch(pitch):
    pitch_values = pitch.selected_array['frequency']
    pitch_values = np.trim_zeros(pitch_values)
    pitch_values = list(filter(lambda num: num !=0 and num != 0.0, pitch_values))
    
    if sum(pitch_values) == 0 or len(pitch_values) == 0:
        print("Som não detectado")
        return 0
    
    average = sum(pitch_values) / len(pitch_values)
    # sp for single_pitch
    if LOG_TYPE == 'full':
        for sp in pitch_values:
            print("Hz: {}".format(sp))
            
    if LOG_TYPE == 'full' or LOG_TYPE == 'short':
        print("Média de Hz: {}".format(average))
    
    return average
  
# Using this website as reference: https://pages.mtu.edu/~suits/notefreqs.html
# Detecting C3(Bb3), D3(), E3, C4, D4, E4
# Referencia: 220 - 233.08 Hz + 246.94
# 220 - 233.08 = 13.08. /2 = 6.54
# 246.94 - 233.08 = 13.86. /2 = 6.93
# ValorMínimo = F_{atual} - \left| \frac{(F_{ant} - F_{atual})}{2} \right|
# ValorMáximo = \left| \frac{(F_{prox} - F_{atual})}{2} \right| + F_{atual}
def detect_note(pitch):
    # Bb3 - 233.08 Hz |- 6.54| |+ 6.93|
    if pitch > 226.54 and pitch < 240.01:
        return "C4"

    # Bb4 - 466.16 Hz |- 13.08| |+ 13.86|
    if pitch > 453.08 and pitch < 480.02:
        return "C5"
    
    # C4 - 261.63 Hz |- 7.345| |+ 7.775|
    if pitch > 254.285 and pitch < 269.405:
        # afinacao = pitch - 261.63
        return "D4"

    # C5 - 523.25 Hz |- 14.685| |+ 15.56|
    if pitch > 508.565 and pitch < 538.81:
        return "D5"

    # D4 - 293.66 Hz |- 8.24| |+ 8.735| 
    if pitch > 285.42 and pitch < 302.395:
        return "E4"

    # D5 - 587.33 Hz |- 16.48| |+ 17.46|
    if pitch > 570.85 and pitch < 604.79:
        return "E5"
    
    # return "Nota fora do escopo"
    return "-"
      
# pitch = snd.to_pitch()

# average = average_pitch(pitch)
# print("pitch: {}".format(detect_note(average)))

acuraciaIndividual = {
    "C4": {"length": 0, "notascorretas": 0, "acuracia" : 0},
    "C5": {"length": 0, "notascorretas": 0, "acuracia" : 0},
    "D4": {"length": 0, "notascorretas": 0, "acuracia" : 0},
    "D5": {"length": 0, "notascorretas": 0, "acuracia" : 0},
    "E4": {"length": 0, "notascorretas": 0, "acuracia" : 0},
    "E5": {"length": 0, "notascorretas": 0, "acuracia" : 0}
};

for dirpath, dirnames, filenames in os.walk(DATASET_PATH):
  if dirpath is not DATASET_PATH and "MP3" not in dirpath:
    dirpath_components = dirpath.split('/')
    label = dirpath_components[-1]
    for filename in filenames:
        snd = parselmouth.Sound(dirpath+'/'+filename)
        pitch = snd.to_pitch()
        average = average_pitch(pitch)
        detected = detect_note(average)
        correta = 1 if detected == label else 0
        acuraciaIndividual[label]["length"] = acuraciaIndividual[label]["length"] + 1
        acuraciaIndividual[label]["notascorretas"] = acuraciaIndividual[label]["notascorretas"] + correta
        print("pitch: {}".format(detect_note(average)))

# Equação 3
acuraciaIndividual["C4"]["acuracia"] = (acuraciaIndividual["C4"]["notascorretas"] * 100)/acuraciaIndividual["C4"]["length"]
acuraciaIndividual["C5"]["acuracia"] = (acuraciaIndividual["C5"]["notascorretas"] * 100)/acuraciaIndividual["C5"]["length"]
acuraciaIndividual["D4"]["acuracia"] = (acuraciaIndividual["D4"]["notascorretas"] * 100)/acuraciaIndividual["D4"]["length"]
acuraciaIndividual["D5"]["acuracia"] = (acuraciaIndividual["D5"]["notascorretas"] * 100)/acuraciaIndividual["D5"]["length"]
acuraciaIndividual["E4"]["acuracia"] = (acuraciaIndividual["E4"]["notascorretas"] * 100)/acuraciaIndividual["E4"]["length"]
acuraciaIndividual["E5"]["acuracia"] = (acuraciaIndividual["E5"]["notascorretas"] * 100)/acuraciaIndividual["E5"]["length"]
    
print("acuracia: {}".format(acuraciaIndividual))

# Equação 4
somaAcuracias = acuraciaIndividual["C4"]["acuracia"] + acuraciaIndividual["C5"]["acuracia"] + acuraciaIndividual["D4"]["acuracia"] + acuraciaIndividual["D5"]["acuracia"] + acuraciaIndividual["E4"]["acuracia"] + acuraciaIndividual["E5"]["acuracia"]
print("total: {}".format(somaAcuracias/6))