import sys, signal
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
    
#######################   Listen  #################################
import speech_recognition as sr 
import wave

def listen_to_me(threshold=3000):
    # used speech_recognition to control audio input
    # Github:   https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__init__.py
    # Documentation:  https://pypi.org/project/SpeechRecognition/1.2.3/
    
    url,x_header = xunfei_preparation()                                                                  
    r = sr.Recognizer()
    r.energy_threshold = threshold   # threshold for background noise
#     r.pause_threshold = 0.8   # minimum length of silence (in seconds) that will register as the end of a phrase.  
    
    while True:
        with sr.Microphone() as source:                                                                 
            print("I am listening....")
            # r.listen start recording when there is audio input higher than threshold (set this to a reasonable number),
            # and stops recording when silence >0.8s(changable)
            audio = r.listen(source)
            
            # get wav data from AudioData object 
            wav = audio.get_wav_data(convert_rate = 16000,convert_width=2) # width=2 gives 16bit audio.
            print('Got it. Recognizing....')
        try:
#             print("You said :\n" + r.recognize_google(audio))
            word = xunfei_recognition(wav,url,x_header)
            print(word)
        except sr.UnknownValueError:
            print("Could not understand audio\nTurning on Silence Mode...")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

            
###########################  Recognition   ######################################
import urllib.parse, urllib.request
import time
import json
import hashlib
import base64

def xunfei_preparation():
    url = 'https://api.xfyun.cn/v1/service/v1/iat'
    api_key = '008d375d21d042a7af90dc31520ae6f5'  # api key在这里
    x_appid = '5b6e5b3e'  # appid在这里
    param = {"engine_type": "sms16k", "aue": "raw"}
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_checksum_content = api_key + str(x_time) + str(x_param, 'utf-8')
    x_checksum = hashlib.md5(x_checksum_content.encode('utf-8')).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    return url,x_header

def xunfei_recognition(audio,url,headers):
    
    base64_audio = base64.b64encode(audio)
    body = urllib.parse.urlencode({'audio': base64_audio})

    req = urllib.request.Request(url=url, data=body.encode('utf-8'), headers=headers, method='POST')
    result = urllib.request.urlopen(req)
    result = result.read().decode('utf-8')
    result = json.loads(result)
    print(result)
    return (result['data'])

listen_to_me()
