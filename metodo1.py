# Método 1:
# Detecta manualmente a afinação da anota, se é um Dó, Ré ou Mi.

#Imports
import parselmouth
import numpy as np
from detect_sound import WAVE_OUTPUT_FILENAME, detect_audio


# Variavel Global
AFINACAO_RANGE = 2
# full, short, hard
LOG_TYPE = "short"


detect_audio()

# Pega a música:
# snd = parselmouth.Sound("./Escala Cromatica - video youtube/E4.mp3")
#   snd = parselmouth.Sound("./Variações Dó/Dó 4t/J Arban Pag 12 N.7 C3 1.mp3")
snd = parselmouth.Sound(WAVE_OUTPUT_FILENAME)

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
        # Quanto mais perto de 233.08, mais afinado.
        afinacao = pitch - 233.08
        if abs(afinacao) > AFINACAO_RANGE:
            return "Nota Real: Bb3. Trompete: C4 - Desafinado - {}".format(afinacao)
        return "Nota Real: Bb3. Trompete: C4 - Afinado"

    # Bb4 - 466.16 Hz |- 13.08| |+ 13.86|
    if pitch > 453.08 and pitch < 480.02:
        afinacao = pitch - 466.16
        if abs(afinacao) > AFINACAO_RANGE:
            return "Nota Real: Bb4. Trompete: C5 - Desafinado - {}".format(afinacao)
        return "Nota Real: Bb4. Trompete: C5 - Afinado"

    # C4 - 261.63 Hz |- 7.345| |+ 7.775|
    if pitch > 254.285 and pitch < 269.405:
        afinacao = pitch - 261.63
        if abs(afinacao) > AFINACAO_RANGE:        
            return "Nota Real: C4. Trompete: D4 - Desafinado : {}".format(afinacao)
        return "Nota Real: C4. Trompete: D4 - Afinado"

    # C5 - 523.25 Hz |- 14.685| |+ 15.56|
    if pitch > 508.565 and pitch < 538.81:
        afinacao = pitch - 523.25
        if abs(afinacao) > AFINACAO_RANGE:        
            return "Nota Real: C5. Trompete: D5 - Desafinado : {}".format(afinacao)
        return "Nota Real: C5. Trompete: D5 - Afinado"

    # D4 - 293.66 Hz |- 8.24| |+ 8.735| 
    if pitch > 285.42 and pitch < 302.395:
        afinacao = pitch - 293.66
        if abs(afinacao) > AFINACAO_RANGE:        
            return "Nota Real: D4. Trompete: E4 - Desafinado : {}".format(afinacao)
        return "Nota Real: D4. Trompete: E4 - Afinado"

    # D5 - 587.33 Hz |- 16.48| |+ 17.46|
    if pitch > 570.85 and pitch < 604.79:
        afinacao = pitch - 587.33
        if abs(afinacao) > AFINACAO_RANGE:        
            return "Nota Real: D5. Trompete: E5 - Desafinado: {}".format(afinacao)
        return "Nota Real: D5. Trompete: E5 - Afinado"
    return "Nota fora do escopo"
      
pitch = snd.to_pitch()

average = average_pitch(pitch)
print("pitch: {}".format(detect_note(average)))