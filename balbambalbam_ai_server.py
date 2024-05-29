# -------------------------- #
# ------- import lib ------- #
# -------------------------- #


import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import speech_recognition as sr
import os
import shutil
import tempfile
from flask import *
import base64
import io
from gtts import gTTS
import wave
from pydub import AudioSegment
from G2P.KoG2Padvanced import KoG2Padvanced
from korean_romanizer.romanizer import Romanizer
import playsound
import requests
from time import sleep
import re




# -------------------------- #
# ------ api key set ------- #
# -------------------------- #

## here is the api key set (secret key)

# -------------------------- #
# --------- method --------- #
# -------------------------- #


# called by <ai/voice>
# generate_voice (text -TTS-> voice -> base64 String)
# using personal pkl, so it is not open source
# so we replace it with gTTS
def generate_voice(text):
    tts = gTTS(text=text, lang='ko', tld='co.kr')
    mp3_data = io.BytesIO()
    tts.write_to_fp(mp3_data)
    mp3_data.seek(0)
    
    mp3_audio = AudioSegment.from_mp3(mp3_data)
    wav_data = io.BytesIO()
    mp3_audio.export(wav_data, format="wav")
    wav_data.seek(0)
    
    base64_encoded_data = base64.b64encode(wav_data.read())
    return base64_encoded_data.decode('utf-8')

def generate_voice_using_tacotron2(gender, age, text):
    # here is the code for Tacotron2
    return correct_audio

# called by <ai/feedback> & <ai/test>
# base64 to wav (base64 String -> wave)
def base64_to_wav_temp(base64_encoded_data):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        wav_data = base64.b64decode(base64_encoded_data)
        temp_file.write(wav_data)
        return temp_file.name
        
def remove_special_characters(text):
    pattern = re.compile('[^\w\s]')
    result = re.sub(pattern, '', text)
    return result
    
    
# called by <ai/feedback> & <ai/test>
# generate_text (STT)
# for more than two characters, use google STT 
# for one character, use RTZR (using secret key, so it is not open source)
def create_user_text(user_audio):
    user_audio_file = base64_to_wav_temp(user_audio)
    r = sr.Recognizer()
    audio_file = sr.AudioFile(user_audio_file)
    with audio_file as source:
        audio = r.record(source)
    return r.recognize_google(audio, language='ko-KR')
    
def create_user_text_using_api(wav_base64):
    # here is the code for STT using api 
    return user_text


# called by <ai/feedback> & <ai/test>
# seperate text (text -> seperated text array)
def seperation_text(text):
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    
    seperated_text = []

    for char in text:
        if char == ' ':
            seperated_text.append(['*', '*', '*'])
        elif '가' <= char <= '힣':
            char_code = ord(char) - 44032
            cho_idx = char_code // 588
            jung_idx = (char_code - (cho_idx * 588)) // 28
            jong_idx = char_code % 28
            seperated_text.append([CHOSUNG_LIST[cho_idx], JUNGSUNG_LIST[jung_idx], JONGSUNG_LIST[jong_idx]])
        else :
            continue

    return seperated_text
    

# called by <ai/test>
# find weak phoneme (text -> weak phoneme array)
def find_weak_phoneme(user_text, correct_text):
    user_weak_phoneme = {}
    user_weak_phoneme_last = {}

    JONGSUNG_MAPPING = {
        'ㄱ': 'ㄱ', 'ㄲ': 'ㄱ', 'ㄳ': 'ㄱ', 'ㄴ': 'ㄴ', 'ㄵ': 'ㄴ', 'ㄶ': 'ㄴ', 
        'ㄷ': 'ㄷ', 'ㄹ': 'ㄹ', 'ㄺ': 'ㄹ', 'ㄻ': 'ㄹ', 'ㄼ': 'ㄹ', 'ㄽ': 'ㄹ', 'ㄾ': 'ㄹ', 'ㄿ': 'ㄹ', 'ㅀ': 'ㄹ', 
        'ㅁ': 'ㅁ', 'ㅂ': 'ㅂ', 'ㅄ': 'ㅂ', 
        'ㅅ': 'ㅅ', 'ㅆ': 'ㅅ', 
        'ㅇ': 'ㅇ', 
        'ㅈ': 'ㄷ', 'ㅊ': 'ㄷ', 'ㅋ': 'ㄱ', 'ㅌ': 'ㄷ', 'ㅍ': 'ㅂ', 'ㅎ': 'ㄷ'
    }

    SIMILAR_JUNGSUNG = {
        'ㅐ': ['ㅔ'], 'ㅔ': ['ㅐ'],
        'ㅙ': ['ㅞ', 'ㅚ'], 'ㅞ': ['ㅙ', 'ㅚ'], 'ㅚ': ['ㅞ', 'ㅙ'],
        'ㅒ': ['ㅖ'], 'ㅖ': ['ㅒ']
    }

    for i, char_correct in enumerate(correct_text):
        if i >= len(user_text):
            user_char = ['*', '*', '*']
        else:
            user_char = user_text[i]
        for j, (ph_correct, ph_user) in enumerate(zip(char_correct, user_char)):
            if ph_correct == ph_user:
                continue
            elif j == 1 and ph_user in SIMILAR_JUNGSUNG.get(ph_correct, []):
                continue
            else:
                if ph_correct not in ['*']:
                    if j != 2:  
                        user_weak_phoneme[ph_correct] = user_weak_phoneme.get(ph_correct, 0) + 1
                    else: 
                        mapped_phoneme = JONGSUNG_MAPPING.get(ph_correct, ph_correct)
                        user_weak_phoneme_last[mapped_phoneme] = user_weak_phoneme_last.get(mapped_phoneme, 0) + 1

    return user_weak_phoneme, user_weak_phoneme_last


# called by <ai/feedback>
# extract duration & draw waveform (base 64 wav String -> base64 img String)
def draw_waveform(user_audio, g_color):
    user_audio_file = base64_to_wav_temp(user_audio)

    with wave.open(user_audio_file, 'r') as wf:
        params = wf.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        audio_data = wf.readframes(nframes)

    samples = np.frombuffer(audio_data, dtype=np.int16)

    non_silent_indices = np.where(np.abs(samples) > 2500)[0]
    start_index = non_silent_indices[0]
    end_index = non_silent_indices[-1]
    non_silent_samples = samples[start_index:end_index]
    original_start_time = 0

    original_end_time = nframes / framerate
    start_time = start_index / framerate
    end_time = end_index / framerate

    original_duration = original_end_time - original_start_time
    duration = end_time - start_time
    time = np.linspace(start_time, end_time, len(non_silent_samples))

    plt.figure(figsize=(10, 4), facecolor='white')
    plt.plot(time, non_silent_samples, color=g_color)
    plt.axis("off")
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    y_lim = 35000 # tmp
    plt.ylim(0, np.max(y_lim))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    plt.close()

    encoded_waveform = base64.b64encode(buf.read()).decode('utf-8')

    # return original_duration, duration, start_time, end_time, encoded_waveform

    return duration, encoded_waveform



# called by <ai/feedback>
# calculate accuracy (correct text, user text -> accuracy)
def calculate_accuracy(correct_text, user_text):
    
    total_chars = 0
    matching_chars = 0
    user_mistaken_index = []
    user_recommend_phoneme = []
    user_recommend_last_phoneme = []
    penalties = 0

    SIMILAR_JUNGSUNG = {
        'ㅐ': ['ㅔ'], 'ㅔ': ['ㅐ'],
        'ㅙ': ['ㅞ', 'ㅚ'], 'ㅞ': ['ㅙ', 'ㅚ'], 'ㅚ': ['ㅞ', 'ㅙ'],
        'ㅒ': ['ㅖ'], 'ㅖ': ['ㅒ']
    }

    for i, correct_char in enumerate(correct_text):
        if i >= len(user_text):
            user_char = ['*', '*', '*']
        else:
            user_char = user_text[i]

        for j, (ph_correct, ph_user) in enumerate(zip(correct_char, user_char)):
            total_chars += 1

            if ph_correct == ph_user:
                matching_chars += 1
            elif j == 1 and ph_user in SIMILAR_JUNGSUNG.get(ph_correct, []):
                matching_chars += 1
            else:
                user_mistaken_index.append(i)
                if j != 2:  
                    user_recommend_phoneme.append(ph_correct)
                else: 
                    user_recommend_last_phoneme.append(ph_correct)

    if len(correct_text) < len(user_text) :
        for j in range(i+1, len(user_text)):
            penalties +=10
            user_mistaken_index.append(j)

    accuracy = int((matching_chars / total_chars) * 100) - penalties
    if accuracy < 0 :
        accuracy = 0
        
    if (int((matching_chars / total_chars) * 100) == 100) and (penalties > 0) :
        user_recommend_phoneme.append('-1')
        
    user_mistaken_index = list(set(user_mistaken_index))
    user_recommend_phoneme = list(set(user_recommend_phoneme))
    user_recommend_last_phoneme = list(set(user_recommend_last_phoneme))

    user_recommend_phoneme = [phoneme for phoneme in user_recommend_phoneme if phoneme != ' ']
    user_recommend_last_phoneme = [phoneme for phoneme in user_recommend_last_phoneme if phoneme != ' ']
    user_recommend_phoneme = [phoneme for phoneme in user_recommend_phoneme if phoneme != '*']
    user_recommend_last_phoneme = [phoneme for phoneme in user_recommend_last_phoneme if phoneme != '*']

    return accuracy, user_mistaken_index, user_recommend_phoneme, user_recommend_last_phoneme

  
    
# called by <ai/kor-pronunciation>
# generate pronunciation (kor text -> kor pronunciation) 
def generate_kor_pronunciation(text):
    return KoG2Padvanced(text)
    
    
# called by <ai/eng-pronunciation>
# generate eng pronunciation (kor text -> eng pronunciation)
def generate_eng_pronunciation(text):
    r = Romanizer(remove_special_characters(text))
    return r.romanize()


# -------------------------- #
# ------ flask server ------ #
# -------------------------- #


# <ai/feedback> HTTP Request Handler (POST)
app = Flask(__name__)
@app.route("/ai/feedback",methods=["POST"])
def get_feedback_request():
    print("=== request : ai/feedback ===")

    # get request data
    data = request.json
    if data is None:
        print("Missing parameters")
        return "Missing parameters", 400

    # get parameters
    try : 
        user_audio = data.get("userAudio")
        correct_audio = data.get("correctAudio")
        correct_text = data.get("pronunciation") 
        print("request text : ", correct_text)
    except Exception as e:
        print("Invalid parameters")
        return "Invalid parameters", 400
    
    # extract user text
    try : 
        # using STT
        if len(correct_text) == 1 :
            user_text = create_user_text_using_api(user_audio)
        else : 
            user_text = create_user_text(user_audio)
            
        # trim whitespace  
        if len(correct_text) < 5:
            user_text = re.sub(r"\s+", "", user_text)
        
        # print user_text
        print("user text : ", user_text)
        
        # exception
        if len(user_text) == 1:
            if len(user_text) > len(correct_text)*3 :
                raise ValueError("User text is too long")
        elif len(user_text) >= len(correct_text)*2 :
            raise ValueError("User text is too long")
        elif len(user_text)*2 < len(correct_text) :
            raise ValueError("User text is too short")

    except ValueError as ve:
        print(ve)
        return f"{ve}, please request re-recording", 422
    except Exception as e:
        print("failed to extract user text (STT)")
        return "failed to extract user text (STT), please request re-recording", 422

    # seperation text
    try :
        seperated_user_text = seperation_text(user_text)
        seperated_correct_text = seperation_text(correct_text)
    except Exception as e:
        print("failed to seperate text")
        return "failed to seperate text", 500

    # calculate accuracy, extract mistaken index & phoneme
    try : 
        user_accuracy, user_mistaken_index, user_recommend_phoneme, user_recommend_last_phoneme = calculate_accuracy(seperated_correct_text, seperated_user_text)
        print("Accuracy:", user_accuracy)
        print("Mistaken indices:", user_mistaken_index)
        print("Mistaken phonemes:", user_recommend_phoneme)
        print("Mistaken last phonemes:", user_recommend_last_phoneme)
    except Exception as e:
        print("failed to calculate accuracy")
        return "failed to calculate accuracy", 500
    
    # extract duration & draw waveform
    try : 
        user_audio_duration, user_audio_waveform = draw_waveform(user_audio, '#644829')
        correct_audio_duration, correct_audio_waveform = draw_waveform(correct_audio, '#ED7161')   

        print("User audio duration:", user_audio_duration)
        print("Correct audio duration:", correct_audio_duration)  
    except Exception as e:
        print("failed to extract duration & draw waveform")
        return "failed to extract duration & draw waveform", 500

    # make output data
    output_data = {
        "userText": user_text,
        "userMistakenIndexes": user_mistaken_index,
        "userAccuracy": user_accuracy,
        "recommendedPronunciations": user_recommend_phoneme,
        "recommendedLastPronunciations": user_recommend_last_phoneme,
        "userWaveform": user_audio_waveform,
        "userAudioDuration": user_audio_duration,
        "correctWaveform": correct_audio_waveform,
        "correctAudioDuration": correct_audio_duration
    }
    print("=== fin : ai/feedback ===")
    return Response(json.dumps(output_data, ensure_ascii=False, indent=4), status = 200, mimetype = 'application/json')


# <ai/voice> HTTP Request Handler (POST)
@app.route("/ai/voice",methods=["POST"])
def get_voice_request():
    print("=== request : ai/voice ===")

    # get request data
    data = request.json
    if data is None:
        print("Missing parameters")
        return "Missing parameters", 400

    # get parameters
    try : 
        gender = data.get("gender")
        age = data.get("age")
        text = data.get("text")
        print("age : ", age)
        print("gender : ", gender)
        print("request text : ", text)
    except Exception as e:
        print("Invalid parameters")
        return "Invalid parameters", 400
    
    # generate voice
    try : 
        correct_audio = generate_voice(text)
        # correct_audio = generate_voice_using_tacotron2(gender, age, text)
    except Exception as e:
        print("failed to generate voice (TTS)")
        return "failed to generate voice (TTS)", 500
    
    # make output data
    output_data = {
        "correctAudio": correct_audio,
    }
    print(len(correct_audio))
    print("=== fin : ai/voice ===")
    return Response(json.dumps(output_data, ensure_ascii=False, indent=4), status = 200, mimetype = 'application/json')
    

# <ai/test> HTTP Request Handler (POST)
@app.route("/ai/test",methods=["POST"])
def get_test_request():
    print("=== request : ai/test ===")
    # get request data
    data = request.json
    if data is None:
        print("Missing parameters")
        return "Missing parameters", 400

    # get parameters
    try :
        user_audio = data.get("userAudio")
        correct_text = data.get("correctText")  
        print("request text : ", correct_text)
    except Exception as e:
        print("Invalid parameters")
        return "Invalid parameters", 400
        
    # extract user text
    try : 
        if len(correct_text) == 1 :
            user_text = create_user_text_using_api(user_audio)
        else : 
            user_text = create_user_text(user_audio)
        print("user text : ", user_text)
        
        if len(user_text) >= len(correct_text)*2 :
            raise ValueError("User text is too long")
    
        if len(user_text)*2 < len(correct_text) :
            raise ValueError("User text is too short")
    
    except ValueError as ve:
        print(ve)
        return f"{ve}, please request re-recording", 422
    except Exception as e:
        print("failed to extract user text (STT)")
        return "failed to extract user text (STT), please request re-recording", 422

    # seperation text
    try :
        seperated_user_text = seperation_text(user_text)
        seperated_correct_text = seperation_text(correct_text)
    except Exception as e:
        print("failed to seperate text")
        return "failed to seperate text", 500

    # find weak phoneme
    try : 
        user_weak_phoneme, user_weak_phoneme_last = find_weak_phoneme(seperated_user_text, seperated_correct_text)  
        print("user weak phoneme : ", user_weak_phoneme)
        print("user_weak_phoneme_last : ", user_weak_phoneme_last)
    except Exception as e:
        print("failed to find weak phoneme")
        return "failed to find weak phoneme", 500

    # make output data
    output_data = {
        "userWeakPhoneme": user_weak_phoneme,
        "userWeakPhonemeLast": user_weak_phoneme_last,
        "userText": user_text,
    }
    print("=== fin : ai/test ===")
    return Response(json.dumps(output_data, ensure_ascii=False, indent=4), status = 200, mimetype = 'application/json')


# <ai/kor-pronunciation> HTTP Request Handler (POST)
@app.route("/ai/kor-pronunciation",methods=["POST"])
def get_kor_pronunciation_request():
    print("=== request : ai/kor-pronunciation ===")
    
    data = request.json
    if data is None:
        print("Missing parameters")
        return "Missing parameters", 400
        
    try :
        text = data.get("text")
        print("request text : ", text)
    except Exception as e:
        print("Invalid parameters")
        return "Invalid parameters", 400
    
    try : 
        kor_pronunciation = generate_kor_pronunciation(text)
        print("kor-pronunciation : ", kor_pronunciation)
    except Exception as e:
        print("failed to generate pronunciation")
        return "failed to generate pronunciation", 500
   
        
    output_data = {
        "korPronunciation": kor_pronunciation
    }
    
    print("=== fin : ai/kor-pronunciation ===")
    return Response(json.dumps(output_data, ensure_ascii=False, indent=4), status = 200, mimetype = 'application/json')

# <ai/eng-pronunciation> HTTP Request Handler (POST)
@app.route("/ai/eng-pronunciation",methods=["POST"])
def get_eng_pronunciation_request():
    print("=== request : ai/eng-pronunciation ===")
    
    data = request.json
    if data is None:
        print("Missing parameters")
        return "Missing parameters", 400
        
    try :
        text = data.get("text")
        print("request text : ", text)
    except Exception as e:
        print("Invalid parameters")
        return "Invalid parameters", 400
    
    try : 
        eng_pronunciation = generate_eng_pronunciation(text)
        print("eng-pronunciation : ", eng_pronunciation)
    except Exception as e:
        print("failed to generate pronunciation")
        return "failed to generate pronunciation", 500
        
    output_data = {
        "engPronunciation": eng_pronunciation,
    }
    
    print("=== fin : ai/eng-pronunciation ===")
    return Response(json.dumps(output_data, ensure_ascii=False, indent=4), status = 200, mimetype = 'application/json')


# -------------------------- #
# ---------- main ---------- #
# -------------------------- #


# main function (run server)
if __name__ == "__main__":
    # example running code (for real, use your own ip address)
    app.run(host = "0.0.0.0", port = 5000, debug = True)