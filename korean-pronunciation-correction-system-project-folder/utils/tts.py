import base64
import httpx
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_config

async def generate_voice(gender, age, text):
    config = load_config()
    client_id = config['naver_api_to_tts']['client_id']
    client_secret = config['naver_api_to_tts']['client_secret']
    
    # Determine the speaker based on gender and age
    if gender == 1:
        if age <= 14:
            speaker = 'vdain'       # Female child
        elif age <= 40:
            speaker = 'nkyunglee'   # Female young adult
        else:
            speaker = 'nsunkyung'   # Female middle-aged or older
    elif gender == 0:
        if age <= 14:
            speaker = 'nhajun'      # Male child
        elif age <= 40:
            speaker = 'vdaeseong'   # Male young adult
        else:
            speaker = 'nyoungil'    # Male middle-aged or older
    else:
        speaker = 'nkyunglee'       # Default speaker

    # Prepare the request data
    request_data = {
        "speaker": speaker,
        "volume": 5,
        "speed": 2,
        "pitch": 0,
        "format": "wav",
        "text": text
    }
    
    # Prepare the request headers
    request_headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post("https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts", 
                                     data=request_data, 
                                     headers=request_headers)
    
    # Check the response status
    if response.status_code == 200:
        print("Successfully generated voice.")
        # Encode the response content to base64
        return base64.b64encode(response.content).decode('utf-8')
    else:
        print(f"Error Code: {response.status_code}")
        return None
